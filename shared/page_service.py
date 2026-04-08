from flask import send_from_directory, abort, render_template
import os

class PageService:
    @staticmethod
    def serve_page(path: str, base_dir: str):
        """Standardized page serving logic for Imza GYO."""
        pages_dir = os.path.join(base_dir, 'pages')
        
        # Security: Prevent directory traversal
        if '..' in path or path.startswith('/'):
            abort(400)
            
        # Try serving as a direct file first (e.g. results.html)
        if os.path.isfile(os.path.join(pages_dir, path)):
            if path.endswith('.html'):
                return render_template(path)
            return send_from_directory(pages_dir, path)
            
        # Try appending .html (e.g. /detay -> detay.html)
        html_path = f"{path}.html"
        if os.path.isfile(os.path.join(pages_dir, html_path)):
            return render_template(html_path)
            
        abort(404)
