from flask import Blueprint, request, jsonify, render_template, current_app
import jwt
from datetime import datetime, timedelta
import json
from shared.database import get_db_connection

compass_bp = Blueprint('compass', __name__)

def generate_magic_link(lead_id):
    payload = {
        'lead_id': lead_id,
        'exp': datetime.utcnow() + timedelta(days=30)
    }
    token = jwt.encode(payload, current_app.secret_key, algorithm='HS256')
    return token

def decode_magic_link(token):
    try:
        payload = jwt.decode(token, current_app.secret_key, algorithms=['HS256'])
        return payload.get('lead_id')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# API to generate link (for admins)
@compass_bp.route('/generate-link/<int:lead_id>', methods=['POST'])
def create_link(lead_id):
    token = generate_magic_link(lead_id)
    url = f"{request.host_url}pusula/{token}"
    return jsonify({'url': url, 'token': token})

# Frontend Route
@compass_bp.route('/pusula/<token>')
def pusula_dashboard(token):
    lead_id = decode_magic_link(token)
    if not lead_id:
        return "Geçersiz veya süresi dolmuş bağlantı. Lütfen danışmanınızdan yeni bir link isteyin.", 403
    return render_template('compass-dashboard.html', token=token)

@compass_bp.route('/data', methods=['GET'])
def get_compass_data():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Token bulunamadı'}), 401
    
    token = auth_header.split(' ')[1]
    lead_id = decode_magic_link(token)
    if not lead_id:
        return jsonify({'error': 'Geçersiz token'}), 403

    from shared.database import get_db
    with get_db() as conn:
        lead = conn.execute('SELECT name, interest_property_id, status, created_at FROM leads WHERE id = ?', (lead_id,)).fetchone()
        if not lead:
            return jsonify({'error': 'Lead bulunamadı'}), 404

        # Property Stats
        property_data = None
        stats = {'views': 124, 'calculations': 3, 'favorites': 12}
        
        if lead['interest_property_id']:
            # Using standardized English field names (Phase 13)
            prop = conn.execute('SELECT id, baslik1 as title, resim_hero as image_url, fiyat as price FROM portfoyler WHERE id = ?', (lead['interest_property_id'],)).fetchone()
            if prop:
                property_data = dict(prop)

        # Timeline (Public filtered)
        timeline = []
        
        ph_rows = conn.execute('''
            SELECT ph.created_at, ps.name as stage_name
            FROM pipeline_history ph
            JOIN pipeline_stages ps ON ph.new_stage_id = ps.id
            WHERE ph.lead_id = ?
        ''', (lead_id,)).fetchall()
        
        for row in ph_rows:
            timeline.append({
                'type': 'pipeline',
                'timestamp': row['created_at'],
                'title': f"Aşama Güncellendi: {row['stage_name']}",
                'description': "İşleminiz bu aşamaya taşındı."
            })
            
        timeline.append({
            'type': 'system',
            'timestamp': lead['created_at'],
            'title': 'Süreciniz Başladı',
            'description': 'İmza GYO Dijital Yaşam Yolculuğuna hoş geldiniz.'
        })

        # Sort chronologically (newest first)
        timeline.sort(key=lambda x: x['timestamp'], reverse=True)

        return jsonify({
            'lead_name': lead['name'],
            'property': property_data,
            'stats': stats,
            'timeline': timeline,
            'status': lead['status']
        }), 200
