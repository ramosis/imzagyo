from typing import Optional, List, Dict, Any
import uuid
import json
from flask import request, jsonify, g
from shared.database import get_db
from shared.extensions import cache
from shared.utils import api_error, invalidate_entity_cache
from modules.ai.routes import translate_content
from shared.utils import sanitize_input, sanitize_html
from shared.schemas import portfolio_schema, ValidationError
from modules.auth.decorators import require_permission, login_required
from . import portfolio_bp

from .repository import PortfolioRepository
from .service import PortfolioService

def get_portfolio_cache_key():
    from modules.auth.service import AuthService
    user = AuthService.get_current_user()
    circle = user.get('circle', 'public') if user else 'public'
    lang = request.args.get('lang', 'tr').lower()
    return f"portfolios_{circle}_{lang}_{request.full_path}"

@portfolio_bp.route('/portfolios', methods=['GET'])
@cache.cached(timeout=300, key_prefix=get_portfolio_cache_key)
def get_portfolios():
    from modules.auth.service import AuthService
    user = AuthService.get_current_user()
    
    filters = {}
    if user and user.get('circle') == 'outer':
        filters['owner_id'] = user['id']
        
    rows = PortfolioRepository.get_all(filters=filters)
    lang = request.args.get('lang', 'tr').lower()
    portfolios = []
    for row in rows:
        d = dict(row)
        if lang in ['en', 'ar']:
            for field in ['baslik1', 'baslik2', 'lokasyon', 'hikaye']:
                override = d.get(f'{field}_{lang}')
                if override: d[field] = override
        if d.get('ozellikler'):
            try: d['ozellikler_arr'] = json.loads(d['ozellikler'])
            except: d['ozellikler_arr'] = []
        portfolios.append(d)
    return jsonify(portfolio_schema.dump(portfolios, many=True))

@portfolio_bp.route('/portfolios/<id>', methods=['GET'])
@cache.memoize(timeout=600)
def get_portfolio(id):
    portfolio = PortfolioRepository.get_by_id(id)
    if not portfolio:
        return api_error("NOT_FOUND", "Portfolio not found", status_code=404)
    d = dict(portfolio)
    lang = request.args.get('lang', 'tr').lower()
    if lang in ['en', 'ar']:
        for field in ['baslik1', 'baslik2', 'lokasyon', 'hikaye']:
            override = d.get(f'{field}_{lang}')
            if override: d[field] = override
    if d.get('ozellikler'):
        try: d['ozellikler_arr'] = json.loads(d['ozellikler'])
        except: d['ozellikler_arr'] = []
    return jsonify(portfolio_schema.dump(d))

@portfolio_bp.route('/portfolios', methods=['POST'])
@require_permission('admin')
def create_portfolio():
    try:
        validated_data = PortfolioService.process_and_create(request.json)
        invalidate_entity_cache('portfolio')
        return jsonify(validated_data), 201
    except ValidationError as err:
        return api_error("VALIDATION_ERROR", "Zorunlu alanlar eksik", details=err.messages, status_code=400)
    except Exception as e:
        return api_error("INTERNAL_ERROR", str(e), status_code=500)

@portfolio_bp.route('/portfolios/<id>', methods=['PUT'])
@require_permission('portfolio.edit')
def update_portfolio(id):
    user = g.user
    if not PortfolioService.can_manage_portfolio(user, id):
        return api_error("FORBIDDEN", "Unauthorized - Owner only", status_code=403)
    try:
        sanitized_data = sanitize_input(request.json)
        update_data = portfolio_schema.load(sanitized_data, partial=True)
        target_fields = ['baslik1', 'baslik2', 'lokasyon', 'hikaye']
        for field in target_fields:
            if field in update_data:
                source = update_data[field]
                update_data[f'{field}_en'] = translate_content(source, 'İngilizce')
                update_data[f'{field}_ar'] = translate_content(source, 'Arapça')
        if PortfolioRepository.update(id, update_data):
            cache.delete_memoized(get_portfolio, id)
            cache.clear()
            return jsonify({'status': 'updated'}), 200
        return api_error("NOT_FOUND", "Portfolio not found", status_code=404)
    except ValidationError as err:
        return api_error("VALIDATION_ERROR", "Invalid update data", details=err.messages)
    except Exception as e:
        return api_error("SERVER_ERROR", str(e), status_code=500)

@portfolio_bp.route('/portfolios/<id>', methods=['DELETE'])
@require_permission('portfolio.delete')
def delete_portfolio(id):
    user = g.user
    if not PortfolioService.can_manage_portfolio(user, id):
        return api_error("FORBIDDEN", "Unauthorized - Owner only", status_code=403)
    if PortfolioRepository.delete(id):
        cache.delete_memoized(get_portfolio, id)
        cache.clear()
        return jsonify({"status": "deleted"}), 200
    return api_error("NOT_FOUND", "Portfolio not found", status_code=404)
