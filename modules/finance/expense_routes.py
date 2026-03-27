from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import login_required, require_inner_circle
from . import finance_bp

# Personnel Expenses
@finance_bp.route('/expenses', methods=['GET'])
@login_required
def get_expenses():
    user = g.user
    with get_db() as conn:
        if user['role'] in ['admin', 'super_admin']:
            query = 'SELECT e.*, u.username FROM expenses e LEFT JOIN users u ON e.user_id = u.id ORDER BY e.date DESC'
            expenses = conn.execute(query).fetchall()
        else:
            query = 'SELECT e.*, u.username FROM expenses e LEFT JOIN users u ON e.user_id = u.id WHERE e.user_id = ? ORDER BY e.date DESC'
            expenses = conn.execute(query, (user['id'],)).fetchall()
    return jsonify([dict(e) for e in expenses]), 200

@finance_bp.route('/expenses', methods=['POST'])
@login_required
def add_expense():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO expenses (user_id, category, amount, description, receipt_image, date, status)
            VALUES (?,?,?,?,?,?,?)
        ''', (g.user['id'], data.get('category'), data.get('amount'), data.get('description'), 
              data.get('receipt_image'), data.get('date'), 'pending'))
        conn.commit()
    return jsonify({'status': 'created'}), 201

@finance_bp.route('/expenses/<int:id>/approve', methods=['PUT'])
@require_inner_circle
def approve_expense(id):
    with get_db() as conn:
        conn.execute("UPDATE expenses SET status = 'approved' WHERE id = ?", (id,))
        conn.commit()
    return jsonify({'status': 'approved'}), 200

# Property Taxes
@finance_bp.route('/taxes', methods=['GET'])
@require_inner_circle
def get_taxes():
    with get_db() as conn:
        query = 'SELECT t.*, p.baslik1, p.refNo FROM taxes t LEFT JOIN portfoyler p ON t.property_id = p.id'
        taxes = conn.execute(query).fetchall()
    return jsonify([dict(t) for t in taxes]), 200

@finance_bp.route('/taxes', methods=['POST'])
@require_inner_circle
def add_tax():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO taxes (property_id, tax_type, amount, due_date, status) VALUES (?,?,?,?,?)',
                    (data.get('property_id'), data.get('tax_type'), data.get('amount'), data.get('due_date'), data.get('status')))
        conn.commit()
    return jsonify({'status': 'created'}), 201
