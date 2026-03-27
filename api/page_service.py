import os
import json
from flask import send_from_directory, request, abort, render_template_string
from shared.database import get_db

class PageService:
    @staticmethod
    def serve_page(path, base_dir):
        """
        Handles SEO rewriting, static file serving, and HTML injection.
        """
        if path.startswith('api/'):
            return "Not Found", 404

        pages_dir = os.path.join(base_dir, 'pages')
        
        # 1. SEO Rewriting Logic
        parts = path.strip('/').split('/')
        known_cities = ['kutahya', 'istanbul', 'ankara', 'izmir']
        
        # Example pattern: /kutahya/-1-villa-merkez
        if parts[0] in known_cities and len(parts) > 1:
            slug = parts[1]
            if '-' in slug:
                # Extract ID from slug (usually starts with -ID-)
                id_part = slug.split('-')[1]
                # Redirect internally to detay.html with id param
                return PageService.inject_portfolio_metadata(id_part, pages_dir)

        # 2. Standard Page Serving
        clean_path = path if path else 'index.html'
        if not clean_path.endswith('.html') and '.' not in clean_path:
            clean_path += '.html'

        # Special case for detail pages via query param
        if clean_path in ['detay.html', 'detay']:
            prop_id = request.args.get('id')
            if prop_id:
                return PageService.inject_portfolio_metadata(prop_id, pages_dir)

        # Serve static file
        if os.path.exists(os.path.join(pages_dir, clean_path)):
            return send_from_directory(pages_dir, clean_path)
        
        return send_from_directory(pages_dir, '404.html'), 404

    @staticmethod
    def inject_portfolio_metadata(portfolio_id, pages_dir):
        """
        Injects SEO metadata into detay.html based on portfolio data.
        Standardizes on Jinja2-like replacement or simple string replace for now.
        """
        full_html_path = os.path.join(pages_dir, 'detay.html')
        if not os.path.exists(full_html_path):
            return "Detail template missing", 404

        with get_db() as conn:
            portfolio = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (portfolio_id,)).fetchone()
            
        if not portfolio:
            return send_from_directory(pages_dir, '404.html'), 404

        with open(full_html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Standard SEO Dynamic Replacement
        # Use .get() to avoid KeyError if columns are missing in some migrations
        title = f"{portfolio.get('baslik1', 'Detay')} | İmza GYO"
        desc = portfolio.get('baslik2') or f"{portfolio.get('lokasyon', 'Türkiye')} lokasyonunda muhteşem gayrimenkul fırsatı."
        img = portfolio.get('resim_hero') or "/assets/img/default-share.jpg"

        replacements = [
            ('<title>.*?</title>', f'<title>{title}</title>'),
            ('<meta property="og:title" content=".*?">', f'<meta property="og:title" content="{title}">'),
            ('<meta property="og:description" content=".*?">', f'<meta property="og:description" content="{desc}">'),
            ('<meta property="og:image" content=".*?">', f'<meta property="og:image" content="{img}">'),
            ('<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">')
        ]

        import re
        for pattern, replacement in replacements:
            html_content = re.sub(pattern, replacement, html_content, flags=re.IGNORECASE)

        return html_content
