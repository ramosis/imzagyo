from flask import Blueprint, request, jsonify, g
from database import get_db_connection
from api.auth import require_inner_circle, get_current_user
import json

projects_bp = Blueprint('projects', __name__)

# --- ADMIN ENDPOINTS ---

@projects_bp.route('/api/projects', methods=['GET'])
@require_inner_circle
def get_projects():
    """Tüm projeleri listeler (Admin)."""
    conn = get_db_connection()
    projects = conn.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(p) for p in projects]), 200

@projects_bp.route('/api/projects', methods=['POST'])
@require_inner_circle
def create_project():
    """Yeni bir landing page projesi oluşturur (Admin)."""
    data = request.json
    if not data or not data.get('slug') or not data.get('name'):
        return jsonify({'error': 'Slug and Name are required'}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            INSERT INTO projects (slug, name, description, hero_image_url, theme_color, features, price_range, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['slug'],
            data['name'],
            data.get('description'),
            data.get('hero_image_url'),
            data.get('theme_color', '#b99860'),
            json.dumps(data.get('features', [])),
            data.get('price_range'),
            data.get('location')
        ))
        conn.commit()
        new_id = cur.lastrowid
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 400
    
    conn.close()
    return jsonify({'status': 'created', 'id': new_id}), 201

@projects_bp.route('/api/projects/<int:id>/leads', methods=['GET'])
@require_inner_circle
def get_project_leads(id):
    """Belirli bir projeye gelen müşteri taleplerini (Leads) listeler."""
    conn = get_db_connection()
    leads = conn.execute('SELECT * FROM project_leads WHERE project_id = ? ORDER BY created_at DESC', (id,)).fetchall()
    conn.close()
    return jsonify([dict(l) for l in leads]), 200

# --- PUBLIC ENDPOINTS (Landing Page için) ---

@projects_bp.route('/api/projects/public/<slug>', methods=['GET'])
def get_public_project(slug):
    """Ziyaretçinin göreceği proje detaylarını getirir (Slug üzerinden)."""
    conn = get_db_connection()
    project = conn.execute('SELECT * FROM projects WHERE slug = ? AND is_active = 1', (slug,)).fetchone()
    conn.close()
    
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
        
    project_dict = dict(project)
    # JSON string'i list'e çevir
    if project_dict.get('features'):
        try:
            project_dict['features'] = json.loads(project_dict['features'])
        except:
            project_dict['features'] = []
            
    return jsonify(project_dict), 200

@projects_bp.route('/api/projects/public/<slug>/leads', methods=['POST'])
def create_lead(slug):
    """Ziyaretçinin Landing Page üzerinden doldurduğu formu kaydeder."""
    data = request.json
    if not data or not data.get('name') or not data.get('phone'):
        return jsonify({'error': 'Name and Phone are required'}), 400
        
    conn = get_db_connection()
    project = conn.execute('SELECT id FROM projects WHERE slug = ?', (slug,)).fetchone()
    
    if project is None:
        conn.close()
        return jsonify({'error': 'Project not found'}), 404
        
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO project_leads (project_id, name, phone, email, message)
        VALUES (?, ?, ?, ?, ?)
    ''', (project['id'], data['name'], data['phone'], data.get('email'), data.get('message')))
    
    conn.commit()
    conn.close()
    return jsonify({'status': 'success', 'message': 'Talebiniz başarıyla alındı. Teşekkürler!'}), 201
