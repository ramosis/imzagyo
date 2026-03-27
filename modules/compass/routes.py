from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import compass_bp

@compass_bp.route('/heatmaps', methods=['GET'])
@require_inner_circle
def get_heatmaps():
    region = request.args.get('region', 'Kütahya')
    with get_db() as conn:
        data = conn.execute('SELECT * FROM regional_trends WHERE region = ?', (region,)).fetchall()
    return jsonify([dict(d) for d in data])

@compass_bp.route('/opportunities', methods=['GET'])
def get_market_opportunities():
    with get_db() as conn:
        opps = conn.execute('SELECT * FROM portfoyler WHERE is_opportunity = 1 LIMIT 5').fetchall()
    return jsonify([dict(o) for o in opps])
