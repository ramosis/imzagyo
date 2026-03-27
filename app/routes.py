from flask import Blueprint, send_from_directory, request, jsonify
import os
from shared.database import get_db_connection
from api.page_service import PageService

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

@main_bp.route('/<path:path>')
def serve_file(path):
    if not path or path == '/':
        return index()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return PageService.serve_page(path, base_dir)
