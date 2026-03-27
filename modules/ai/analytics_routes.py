from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import ai_bp

@ai_bp.route('/analytics/dashboard', methods=['GET'])
@require_inner_circle
def get_dashboard_stats():
    with get_db() as conn:
        stats = {
            "portfolios": conn.execute('SELECT COUNT(*) FROM portfoyler').fetchone()[0],
            "leads": conn.execute('SELECT COUNT(*) FROM leads').fetchone()[0],
            "active_contracts": conn.execute('SELECT COUNT(*) FROM contracts WHERE status="active"').fetchone()[0]
        }
    return jsonify(stats)

@ai_bp.route('/seo/sitemap', methods=['GET'])
def get_sitemap_data():
    with get_db() as conn:
        portfolios = conn.execute('SELECT id, slug, created_at FROM portfoyler').fetchall()
    return jsonify([dict(p) for p in portfolios])
