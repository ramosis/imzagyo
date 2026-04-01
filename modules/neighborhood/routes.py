from flask import request, jsonify
from . import neighborhood_bp
from .repository import ReservationRepository
# Optional: from modules.auth.decorators import require_auth if authentication is needed for public users.
# Assuming neighborhood endpoints are somewhat public or use basic auth for now.

@neighborhood_bp.route('/reservations/calendar', methods=['GET'])
def get_reservation_calendar():
    facility_id = request.args.get('facility_id', 'gym')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    try:
        reservations = ReservationRepository.get_by_date_range(facility_id, start_date, end_date)
        return jsonify(reservations), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@neighborhood_bp.route('/reservations', methods=['POST'])
def make_reservation():
    data = request.json
    required_fields = ['facility_id', 'date', 'time', 'name']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        res_id = ReservationRepository.create(data)
        return jsonify({"success": True, "reservation_id": res_id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409 # Conflict
    except Exception as e:
        return jsonify({"error": str(e)}), 500
