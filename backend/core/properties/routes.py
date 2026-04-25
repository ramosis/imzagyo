from typing import Optional, List, Dict, Any
import json
from flask import request, jsonify, g
from backend.app.extensions import cache
from shared.utils import api_error, invalidate_entity_cache
from shared.utils import sanitize_input, sanitize_html
from shared.schemas import portfolio_schema, ValidationError
from backend.core.identity.decorators import require_permission, login_required
from . import properties_bp
from .repository import PropertyRepository
from .service import PropertyService

def get_portfolio_cache_key():
    from backend.core.identity.service import IdentityService
    user = IdentityService.get_current_user()
    circle = user.get('circle', 'public') if user else 'public'
    lang = request.args.get('lang', 'tr').lower()
    return f"portfolios_{circle}_{lang}_{request.full_path}"

@properties_bp.route('/', methods=['GET'])
@cache.cached(timeout=300, key_prefix=get_portfolio_cache_key)
def get_properties():
    from backend.core.identity.service import IdentityService
    user = IdentityService.get_current_user()
    
    filters = {}
    if user and user.get('circle') == 'outer':
        filters['owner_id'] = user['id']
        
    rows = PropertyRepository.get_all(filters=filters)
    lang = request.args.get('lang', 'tr').lower()
    portfolios = []
    for row in rows:
        d = dict(row)
        if lang in ['en', 'ar']:
            for field in ['baslik1', 'baslik2', 'lokasyon', 'hikaye']:
                override = d.get(f'{field}_{lang}')
                if override: d[field] = override
        portfolios.append(d)
    return jsonify(portfolio_schema.dump(portfolios, many=True))

@properties_bp.route('/<id>', methods=['GET'])
@cache.memoize(timeout=600)
def get_property(id):
    property_data = PropertyRepository.get_by_id(id)
    if not property_data:
        return api_error("NOT_FOUND", "Property not found", status_code=404)
    d = dict(property_data)
    # ... (Language mapping logic)
    return jsonify(portfolio_schema.dump(d))

@properties_bp.route('/', methods=['POST'])
@require_permission('admin')
def create_property():
    try:
        validated_data = PropertyService.process_and_create(request.json)
        invalidate_entity_cache('portfolio')
        return jsonify(validated_data), 201
    except Exception as e:
        return api_error("INTERNAL_ERROR", str(e), status_code=500)
