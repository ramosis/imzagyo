import json
from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import portfolio_bp

# Admin Endpoints
@portfolio_bp.route('/projects', methods=['GET'])
@require_inner_circle
def get_projects():
    with get_db() as conn:
        projects = conn.execute('SELECT * FROM projects ORDER BY created_at DESC').fetchall()
    return jsonify([dict(p) for p in projects]), 200

@portfolio_bp.route('/projects', methods=['POST'])
@require_inner_circle
def create_project():
    data = request.json
    if not data or not data.get('slug') or not data.get('name'):
        return jsonify({'error': 'Slug and Name are required'}), 400
    try:
        with get_db() as conn:
            cur = conn.cursor()
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
        return jsonify({'status': 'created', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@portfolio_bp.route('/projects/<int:project_id>/leads', methods=['GET'])
@require_inner_circle
def get_project_leads(project_id):
    with get_db() as conn:
        leads = conn.execute('SELECT * FROM project_leads WHERE project_id = ? ORDER BY created_at DESC', (project_id,)).fetchall()
    return jsonify([dict(l) for l in leads]), 200

# Public Endpoints
@portfolio_bp.route('/projects/public/<slug>', methods=['GET'])
def get_public_project(slug):
    with get_db() as conn:
        project = conn.execute('SELECT * FROM projects WHERE slug = ? AND is_active = 1', (slug,)).fetchone()
    if project is None:
        return jsonify({'error': 'Project not found'}), 404
    project_dict = dict(project)
    if project_dict.get('features'):
        try: project_dict['features'] = json.loads(project_dict['features'])
        except: project_dict['features'] = []
    return jsonify(project_dict), 200

@portfolio_bp.route('/projects/public/<slug>/leads', methods=['POST'])
def create_project_lead(slug):
    data = request.json
    if not data or not data.get('name') or not data.get('phone'):
        return jsonify({'error': 'Name and Phone are required'}), 400
    with get_db() as conn:
        project = conn.execute('SELECT id FROM projects WHERE slug = ?', (slug,)).fetchone()
        if project is None:
            return jsonify({'error': 'Project not found'}), 404
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO project_leads (project_id, name, phone, email, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (project['id'], data['name'], data['phone'], data.get('email'), data.get('message')))
        conn.commit()
    return jsonify({'status': 'success', 'message': 'Talebiniz başarıyla alındı.'}), 201
