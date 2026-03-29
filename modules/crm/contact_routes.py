from flask import request, jsonify
from modules.auth.decorators import require_permission
from . import crm_bp
from .repository import ContactRepository

@crm_bp.route('/contacts', methods=['GET'])
@require_permission('admin')
def get_contacts():
    rows = ContactRepository.get_all()
    return jsonify(rows), 200

@crm_bp.route('/contacts', methods=['POST'])
@require_permission('crm.edit')
def add_contact():
    try:
        data = request.json
        ContactRepository.create(data)
        return jsonify({"success": True}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
