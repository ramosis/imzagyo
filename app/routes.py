from flask import Blueprint, send_from_directory, request, jsonify
import os
from shared.database import get_db_connection, get_db, get_setting, set_setting
from shared.page_service import PageService
from shared.utils import sanitize_input

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    host = request.headers.get('Host', '')
    if 'imzamahalle.com' in host:
        return send_from_directory('pages', 'mahalle.html')
    return send_from_directory('pages', 'anasayfa.html')

@main_bp.route('/portal')
def portal():
    return send_from_directory('pages', 'portal.html')

@main_bp.route('/pipeline')
def pipeline():
    return send_from_directory('pages', 'pipeline.html')

@main_bp.route('/mahalle')
def mahalle():
    return send_from_directory('pages', 'mahalle.html')

@main_bp.route('/inspection')
def inspection_page():
    return send_from_directory('pages', 'inspection.html')

@main_bp.route('/admin/analytics')
def admin_analytics_page():
    return send_from_directory('pages', 'admin-analytics.html')

@main_bp.route('/mls')
def mls_page():
    return send_from_directory('pages', 'mls.html')

@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    # This assumes UPLOAD_FOLDER is configured in app.config
    from flask import current_app
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt') # Assuming it's in static now

@main_bp.route('/sitemap.xml')
def sitemap():
    with get_db_connection() as conn:
        portfoyler = conn.execute('SELECT id FROM portfoyler').fetchall()

    base_url = "https://imzaemlak.com"
    pages = [
        {'loc': f"{base_url}/", 'changefreq': 'daily', 'priority': '1.0'},
    ]

    for p in portfoyler:
        pages.append({
            'loc': f"{base_url}/detay?id={p['id']}",
            'changefreq': 'weekly',
            'priority': '0.8'
        })

    sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap_xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in pages:
        sitemap_xml.append(f'  <url><loc>{page["loc"]}</loc><changefreq>{page["changefreq"]}</changefreq><priority>{page["priority"]}</priority></url>')
    sitemap_xml.append('</urlset>')
    
    return "\n".join(sitemap_xml), 200, {'Content-Type': 'application/xml'}

# ========== SETTINGS API ==========
@main_bp.route('/api/v1/settings/site_mode', methods=['GET'])
def get_site_mode():
    """Returns the current site mode."""
    mode = get_setting('site_mode', 'placeholder')
    return jsonify({'site_mode': mode})

@main_bp.route('/api/v1/settings/site_mode', methods=['PUT'])
def set_site_mode():
    """Updates the site mode (admin only)."""
    # Simple admin check via JWT or session
    from modules.auth.service import AuthService
    user = AuthService.get_current_user()
    if not user or user.get('role') not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    new_mode = data.get('site_mode', '').strip().lower()
    if new_mode not in ['demo', 'placeholder', 'live']:
        return jsonify({'error': 'Invalid mode. Must be: demo, placeholder, live'}), 400
    
    set_setting('site_mode', new_mode)
    # Clear portfolio cache
    try:
        from shared.extensions import cache
        cache.clear()
    except Exception:
        pass
    
    return jsonify({'status': 'updated', 'site_mode': new_mode})

# ========== PUBLIC LEAD FORM ==========
@main_bp.route('/api/v1/leads/public', methods=['POST'])
def public_lead_form():
    """Public lead form endpoint - no auth required."""
    from shared.extensions import limiter
    data = request.json or {}
    
    name = sanitize_input(data.get('name', '')).strip() if isinstance(data.get('name', ''), str) else ''
    phone = sanitize_input(data.get('phone', '')).strip() if isinstance(data.get('phone', ''), str) else ''
    email = sanitize_input(data.get('email', '')).strip() if isinstance(data.get('email', ''), str) else ''
    action_type = data.get('action_type', '')  # buy, rent, sell
    notes = sanitize_input(data.get('notes', '')).strip() if isinstance(data.get('notes', ''), str) else ''
    
    if not name or (not phone and not email):
        return jsonify({'error': 'İsim ve en az bir iletişim bilgisi gereklidir.'}), 400
    
    # Map action_type to segment
    segment_map = {
        'buy': 'buyer',
        'rent': 'buyer',
        'sell': 'owner',
        'lease': 'owner'
    }
    segment = segment_map.get(action_type, 'buyer')
    
    with get_db() as conn:
        conn.execute(
            '''INSERT INTO leads (name, phone, email, source, segment, action_type, notes, status)
               VALUES (?, ?, ?, 'website', ?, ?, ?, 'new')''',
            (name, phone, email, segment, action_type, notes)
        )
        conn.commit()
    
    return jsonify({'status': 'success', 'message': 'Bilgileriniz alındı. En kısa sürede sizinle iletişime geçeceğiz.'}), 201

@main_bp.route('/<path:path>')
def serve_file(path):
    if not path or path == '/':
        return index()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return PageService.serve_page(path, base_dir)
