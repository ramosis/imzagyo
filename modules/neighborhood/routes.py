from flask import request, jsonify
from . import neighborhood_bp
from .repository import ReservationRepository
from shared.schemas import lead_schema # placeholder for structural consistency

@neighborhood_bp.route('/reservations/calendar', methods=['GET'])
def get_reservation_calendar():
    """
    Get facility reservation calendar
    ---
    parameters:
      - name: facility_id
        in: query
        type: string
        default: gym
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
    responses:
      200:
        description: List of reservations
      400:
        description: Missing date range
    """
    facility_id = request.args.get('facility_id', 'gym')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    try:
        reservations = ReservationRepository.get_by_date_range(facility_id, start_date, end_date)
        # Serialize ORM objects for JSON response
        results = [{
            "id": r.id,
            "facility_id": r.facility_id,
            "date": r.date,
            "time_slot": r.time_slot,
            "name": r.name,
            "status": r.status
        } for r in reservations]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@neighborhood_bp.route('/reservations', methods=['POST'])
def make_reservation():
    """
    Create a new facility reservation
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            facility_id:
              type: string
            date:
              type: string
            time:
              type: string
            name:
              type: string
            user_id:
              type: integer
    responses:
      201:
        description: Reservation created
      400:
        description: Missing fields
      409:
        description: Capacity reached or slot booked
    """
    data = request.json
    required_fields = ['facility_id', 'date', 'time', 'name']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        res = ReservationRepository.create(data)
        return jsonify({"success": True, "reservation_id": res.id}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 409 # Conflict/Capacity
    except Exception as e:
        return jsonify({"error": str(e)}), 500
