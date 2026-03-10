from flask import Blueprint, request, jsonify
from database import get_db_connection
import json

purchasing_power_bp = Blueprint('purchasing_power', __name__)

@purchasing_power_bp.route('/api/purchasing-power', methods=['POST'])
def save_calculation():
    data = request.json
    conn = get_db_connection()
    
    # Detayları JSON string'e çevir
    details = json.dumps({
        'barter_items': data.get('barter_items', []),
        'credit_used': data.get('use_credit', False)
    })

    conn.execute('''
        INSERT INTO purchasing_power (user_id, cash_amount, credit_amount, barter_total, total_power, details_json)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data.get('user_id', 1), # Varsayılan admin
        data.get('cash_amount', 0),
        data.get('credit_amount', 0),
        data.get('barter_total', 0),
        data.get('total_power', 0),
        details
    ))
    
    conn.commit()
    calc_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    
    return jsonify({'status': 'saved', 'id': calc_id}), 201