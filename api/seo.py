from flask import Blueprint, Response, current_app
from shared.database import get_db_connection
import datetime

seo_bp = Blueprint('seo', __name__)

@seo_bp.route('/sitemap.xml')
def sitemap():
    """Veritabanındaki portföyleri içeren dinamik sitemap üretir."""
    base_url = "https://imzagyo.com" # Canlı domain
    
    pages = [
        {'loc': '/', 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': '/portal', 'changefreq': 'weekly', 'priority': '0.8'},
        {'loc': '/mahalle', 'changefreq': 'weekly', 'priority': '0.7'},
    ]
    
    # Veritabanından portföyleri çek
    conn = get_db_connection()
    portfolios = conn.execute('SELECT id, created_at FROM portfoyler').fetchall()
    conn.close()
    
    for p in portfolios:
        pages.append({
            'loc': f'/portfoy/{p["id"]}',
            'lastmod': p['created_at'].split(' ')[0] if p['created_at'] else datetime.datetime.now().strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6'
        })
        
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    for page in pages:
        xml.append('  <url>')
        xml.append(f'    <loc>{base_url}{page["loc"]}</loc>')
        if 'lastmod' in page:
            xml.append(f'    <lastmod>{page["lastmod"]}</lastmod>')
        xml.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml.append(f'    <priority>{page["priority"]}</priority>')
        xml.append('  </url>')
        
    xml.append('</urlset>')
    
    return Response("\n".join(xml), mimetype='application/xml')
