from flask import Blueprint, jsonify, request, g
from database import get_db_connection
from .auth import require_inner_circle, login_required
import datetime

pipeline_bp = Blueprint('pipeline', __name__)

@pipeline_bp.route('/api/pipeline', methods=['GET'])
@require_inner_circle
def get_pipeline():
    """
    Tüm aşamaları ve içindeki adayları Kanban formatında döndürür.
    """
    conn = get_db_connection()
    
    # 1. Aşamaları al
    stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
    stages_list = [dict(s) for s in stages]
    
    # 2. Adayları al
    leads = conn.execute('''
        SELECT l.id, l.name, l.phone, l.email, l.pipeline_stage_id, l.ai_score, l.status,
               p.baslik1 as property_title, u.username as assigned_to
        FROM leads l
        LEFT JOIN portfoyler p ON l.interest_property_id = p.id
        LEFT JOIN users u ON l.assigned_user_id = u.id
        ORDER BY l.ai_score DESC
    ''').fetchall()
    
    # Gruplama
    for stage in stages_list:
        stage['leads'] = [dict(l) for l in leads if l['pipeline_stage_id'] == stage['id']]
    
    conn.close()
    return jsonify(stages_list)

@pipeline_bp.route('/api/pipeline/stages', methods=['GET'])
@require_inner_circle
def get_stages():
    """Sadece aşama listesini döner."""
    conn = get_db_connection()
    stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
    conn.close()
    return jsonify([dict(s) for s in stages])

@pipeline_bp.route('/api/leads/<int:lead_id>/move', methods=['PUT'])
@login_required
def move_lead(lead_id):
    """
    Bir adayı başka bir aşamaya taşır ve tarihçeye kaydeder.
    """
    data = request.json
    new_stage_id = data.get('stage_id')
    reason = data.get('reason', 'Manuel geçiş')
    user_id = g.user['id']

    if not new_stage_id:
        return jsonify({'error': 'stage_id gereklidir'}), 400

    conn = get_db_connection()
    
    # Mevcut aşamayı al (Tarihçe için)
    lead = conn.execute('SELECT pipeline_stage_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
    if not lead:
        conn.close()
        return jsonify({'error': 'Aday bulunamadı'}), 404
    
    old_stage_id = lead['pipeline_stage_id']
    
    # Güncelleme
    conn.execute('UPDATE leads SET pipeline_stage_id = ? WHERE id = ?', (new_stage_id, lead_id))
    
    # --- Akıllı Bildirim: Danışmana Bilgi Ver ---
    lead_data = conn.execute('SELECT name, assigned_user_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
    if lead_data and lead_data['assigned_user_id']:
        from .notifications import create_notification
        stage_row = conn.execute('SELECT name FROM pipeline_stages WHERE id = ?', (new_stage_id,)).fetchone()
        stage_name = stage_row['name'] if stage_row else 'Bilinmeyen'
        create_notification(
            lead_data['assigned_user_id'], 
            'pipeline', 
            'Huni Aşama Geçişi', 
            f"{lead_data['name']} adlı aday '{stage_name}' aşamasına taşındı."
        )
    
    # Tarihçe Logu
    conn.execute('''
        INSERT INTO pipeline_history (lead_id, old_stage_id, new_stage_id, user_id, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (lead_id, old_stage_id, new_stage_id, user_id, reason))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Aday başarıyla taşındı'})

@pipeline_bp.route('/api/pipeline/insights', methods=['GET'])
@require_inner_circle
def get_pipeline_insights():
    """
    Hunideki tıkanıklıkları ve verimliliği analiz eder.
    """
    conn = get_db_connection()
    
    # Aşama bazlı sayısal dağılım
    stats = conn.execute('''
        SELECT s.name, COUNT(l.id) as count
        FROM pipeline_stages s
        LEFT JOIN leads l ON s.id = l.pipeline_stage_id
        GROUP BY s.id
        ORDER BY s.order_index
    ''').fetchall()
    
    # Ortalama geçiş süresi (Örn: İlk Temas -> Randevu)
    # Bu analiz için pipeline_history verisi kullanılabilir (İleri seviye)
    
    conn.close()
    return jsonify({
        'distribution': [dict(row) for row in stats],
        'total_leads': sum(row['count'] for row in stats)
    })
