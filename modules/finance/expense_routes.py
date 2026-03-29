from flask import request, jsonify, g
from modules.auth.decorators import login_required, require_inner_circle
from . import finance_bp
from .repository import ExpenseRepository, TaxRepository

@finance_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    user = g.user
    is_admin = user['role'] in ['admin', 'super_admin']
    expenses = ExpenseRepository.get_all(user_id=user['id'], is_admin=is_admin)
    return jsonify(expenses), 200

@finance_bp.route('/expenses', methods=['POST'])
@login_required
def add_expense():
    data = request.json
    data['user_id'] = g.user['id']
    ExpenseRepository.create(data)
    return jsonify({'status': 'created'}), 201

@finance_bp.route('/expenses/<int:id>/approve', methods=['PUT'])
@require_inner_circle
def approve_expense(id):
    if ExpenseRepository.update_status(id, 'approved'):
        return jsonify({'status': 'approved'}), 200
    return jsonify({'error': 'Expense not found'}), 404

@finance_bp.route('/taxes', methods=['GET'])
@require_inner_circle
def get_taxes():
    taxes = TaxRepository.get_all()
    return jsonify(taxes), 200

@finance_bp.route('/taxes', methods=['POST'])
@require_inner_circle
def add_tax():
    data = request.json
    TaxRepository.create(data)
    return jsonify({'status': 'created'}), 201
