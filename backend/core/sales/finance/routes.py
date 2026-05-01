from . import finance_bp
from flask import Blueprint, request, jsonify
from backend.shared.database import db_session
from backend.core.identity.auth.decorators import require_permission
from .models import Expense

@finance_bp.route('/api/v1/expenses', methods=['GET'])
@require_permission('admin')
def get_expenses():
    expenses = db_session.query(Expense).order_by(Expense.date.desc()).all()
    return jsonify([{
        'id': e.id,
        'description': e.description,
        'amount': e.amount,
        'currency': e.currency,
        'category': e.category,
        'date': e.date.isoformat()
    } for e in expenses]), 200

@finance_bp.route('/api/v1/revenue', methods=['GET'])
@require_permission('admin')
def get_revenue():
    # Revenue logic would go here
    return jsonify({'total_revenue': 0, 'currency': 'TRY'}), 200
