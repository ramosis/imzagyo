from flask import Blueprint, request, jsonify
from database import get_db_connection

expenses_bp = Blueprint('expenses', __name__)


@expenses_bp.route('/api/expenses', methods=['GET'])
def get_expenses():
    from api.auth import get_current_user
    user = get_current_user()
    if not user:
        return jsonify([]), 401
        
    # Outer circle şirket harcamalarını göremez
    if user.get('circle') == 'outer':
        return jsonify([]), 200

    conn = get_db_connection()

    if user['role'] in ['admin', 'super_admin']:
        # Admin tüm harcamaları görür
        query = '''
            SELECT e.*, u.username
            FROM expenses e
            LEFT JOIN users u ON e.user_id = u.id
            ORDER BY e.date DESC
        '''
        expenses = conn.execute(query).fetchall()
    else:
        # Personel/Danışman sadece kendi harcamalarını görür
        query = '''
            SELECT e.*, u.username
            FROM expenses e
            LEFT JOIN users u ON e.user_id = u.id
            WHERE e.user_id = ?
            ORDER BY e.date DESC
        '''
        expenses = conn.execute(query, (user['id'],)).fetchall()

    conn.close()
    return jsonify([dict(e) for e in expenses]), 200

@expenses_bp.route('/api/expenses', methods=['POST'])
def add_expense():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO expenses (user_id, category, amount, description, receipt_image, date, status)
        VALUES (?,?,?,?,?,?,?)
    ''', (
        data.get('user_id', 1),
        data.get('category'),
        data.get('amount'),
        data.get('description'),
        data.get('receipt_image'),
        data.get('date'),
        'pending'
    ))
    conn.commit()
    expense_id = cur.lastrowid
    conn.close()
    return jsonify({'id': expense_id, 'status': 'created'}), 201

@expenses_bp.route('/api/expenses/<int:id>/approve', methods=['PUT'])
def approve_expense(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE expenses SET status = 'approved' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'approved'}), 200

@expenses_bp.route('/api/expenses/<int:id>/reject', methods=['PUT'])
def reject_expense(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE expenses SET status = 'rejected' WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'rejected'}), 200

@expenses_bp.route('/api/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM expenses WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200
