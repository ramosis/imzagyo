from flask import Blueprint, send_from_directory, request, jsonify, current_app
import os
# from shared.database import get_db_connection, get_db, get_setting, set_setting  # REMOVED TO BREAK CIRCULAR IMPORT
from shared.page_service import PageService
from shared.utils import sanitize_input

main_bp = Blueprint('main', __name__)

# Helper to get the correct path to the project root from modules/core/
def get_root_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

@main_bp.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@main_bp.route('/')
def index():
    host = request.headers.get('Host', '')
    pages_dir = os.path.join(get_root_path(), 'pages')
    if 'imzamahalle.com' in host:
        return send_from_directory(pages_dir, 'mahalle.html')
    return send_from_directory(pages_dir, 'anasayfa.html')

@main_bp.route('/portal')
def portal():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'portal.html')

@main_bp.route('/pipeline')
def pipeline():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'pipeline.html')

@main_bp.route('/mahalle')
def mahalle():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'mahalle.html')

@main_bp.route('/inspection')
def inspection_page():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'inspection.html')

@main_bp.route('/admin/analytics')
def admin_analytics_page():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'admin-analytics.html')

@main_bp.route('/mls')
def mls_page():
    pages_dir = os.path.join(get_root_path(), 'pages')
    return send_from_directory(pages_dir, 'mls.html')

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/robots.txt')
def robots():
    static_dir = os.path.join(get_root_path(), 'static')
    return send_from_directory(static_dir, 'robots.txt')

@main_bp.route('/sitemap.xml')
def sitemap():
    from shared.database import get_db_connection
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
    from shared.database import get_setting
    mode = get_setting('site_mode', 'placeholder')
    return jsonify({'site_mode': mode})

@main_bp.route('/api/v1/settings/site_mode', methods=['PUT'])
def set_site_mode():
    """Updates the site mode (admin only)."""
    from modules.auth.service import AuthService
    user = AuthService.get_current_user()
    if not user or user.get('role') not in ['admin', 'super_admin']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    new_mode = data.get('site_mode', '').strip().lower()
    if new_mode not in ['demo', 'placeholder', 'live']:
        return jsonify({'error': 'Invalid mode. Must be: demo, placeholder, live'}), 400
    
    from shared.database import set_setting
    set_setting('site_mode', new_mode)
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
    data = request.json or {}
    
    name = sanitize_input(data.get('name', '')).strip() if isinstance(data.get('name', ''), str) else ''
    phone = sanitize_input(data.get('phone', '')).strip() if isinstance(data.get('phone', ''), str) else ''
    email = sanitize_input(data.get('email', '')).strip() if isinstance(data.get('email', ''), str) else ''
    action_type = data.get('action_type', '') 
    notes = sanitize_input(data.get('notes', '')).strip() if isinstance(data.get('notes', ''), str) else ''
    
    if not name or (not phone and not email):
        return jsonify({'error': 'İsim ve en az bir iletişim bilgisi gereklidir.'}), 400
    
    segment_map = {'buy': 'buyer', 'rent': 'buyer', 'sell': 'owner', 'lease': 'owner'}
    segment = segment_map.get(action_type, 'buyer')
    
    from shared.database import get_db
    with get_db() as conn:
        conn.execute(
            '''INSERT INTO leads (name, phone, email, source, segment, action_type, notes, status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
            (name, phone, email, 'website', segment, action_type, notes, 'new')
        )
        conn.commit()
    
    return jsonify({'status': 'success', 'message': 'Bilgileriniz alındı. En kısa sürede sizinle iletişime geçeceğiz.'}), 201

@main_bp.route('/<path:path>')
def serve_file(path):
    if not path or path == '/':
        return index()
    base_dir = get_root_path()
    return PageService.serve_page(path, base_dir)
