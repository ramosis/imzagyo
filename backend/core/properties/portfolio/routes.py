import os
from . import portfolio_bp\nfrom flask import Blueprint, request, jsonify, render_template, g
from backend.shared.database import get_db_connection
from backend.app.extensions import cache
from .service import PropertyService
from .repository import PropertyRepository

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/api/v1/properties', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_properties():
    filters = request.args.to_dict()
    lang = request.args.get('lang', 'tr')
    properties = PropertyService.get_filtered_properties(filters, lang)
    return jsonify(properties), 200

@portfolio_bp.route('/api/v1/properties/<int:id>', methods=['GET'])
def get_property_detail(id):
    lang = request.args.get('lang', 'tr')
    property_data = PropertyService.get_property_by_id(id, lang)
    if not property_data:
        return jsonify({'error': 'Property not found'}), 404
    return jsonify(property_data), 200

@portfolio_bp.route('/api/v1/properties', methods=['POST'])
def add_property():
    # Admin check would go here via decorators
    data = request.json
    prop_id = PropertyRepository.create(data)
    return jsonify({'id': prop_id, 'status': 'created'}), 201

@portfolio_bp.route('/api/v1/properties/featured', methods=['GET'])
@cache.cached(timeout=600)
def get_featured_properties():
    lang = request.args.get('lang', 'tr')
    properties = PropertyRepository.get_featured(lang)
    return jsonify(properties), 200

@portfolio_bp.route('/property/<int:id>')
def property_page(id):
    lang = request.args.get('lang', 'tr')
    prop = PropertyService.get_property_by_id(id, lang)
    if not prop:
        return render_template('404.html'), 404
    return render_template('detay.html', property=prop)
