from flask import Blueprint, jsonify

hr_bp = Blueprint('hr', __name__)

@hr_bp.route('/api/hr', methods=['GET'])
def get_hr():
    return jsonify([])
