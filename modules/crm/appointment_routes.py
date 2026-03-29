from flask import request, jsonify
from modules.auth.decorators import require_permission
from . import crm_bp
from .repository import AppointmentRepository

@crm_bp.route('/appointments', methods=['GET'])
@require_permission('admin')
def get_appointments():
    rows = AppointmentRepository.get_all()
    return jsonify(rows), 200

@crm_bp.route('/appointments', methods=['POST'])
@require_permission('crm.edit')
def add_appointment():
    try:
        data = request.json
        AppointmentRepository.create(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
