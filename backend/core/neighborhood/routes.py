from . import neighborhood_bp\nfrom flask import Blueprint, request, jsonify
from backend.shared.database import get_db_connection
from backend.core.identity.auth.decorators import login_required
from .service import NeighborhoodService

neighborhood_bp = Blueprint('neighborhood', __name__)

@neighborhood_bp.route('/api/v1/neighborhood/announcements', methods=['GET'])
def get_announcements():
    announcements = NeighborhoodService.get_announcements()
    return jsonify(announcements), 200

@neighborhood_bp.route('/api/v1/neighborhood/dues', methods=['GET'])
@login_required
def get_dues():
    # User's dues logic
    return jsonify([]), 200

@neighborhood_bp.route('/api/v1/neighborhood/facilities', methods=['GET'])
def get_facilities():
    facilities = NeighborhoodService.get_facilities()
    return jsonify(facilities), 200
