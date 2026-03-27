from flask import Blueprint, request, jsonify
import sqlite3
import json
from shared.database import get_db_connection

inspection_bp = Blueprint('inspection', __name__)

@inspection_bp.route('/api/inspections', methods=['POST'])
def add_inspection():
    data = request.json
    portfolio_id = data.get('portfolio_id')
    staff_id = data.get('staff_id')
    category = data.get('category')
    data_json = json.dumps(data.get('checklist_data'))
    score_summary = json.dumps(data.get('score_summary'))
    overall_score = data.get('overall_score', 0)
    notes = data.get('notes', '')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO property_inspections (portfolio_id, staff_id, category, data_json, score_summary, overall_score, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (portfolio_id, staff_id, category, data_json, score_summary, overall_score, notes))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Denetim başarıyla kaydedildi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@inspection_bp.route('/api/inspections/<portfolio_id>', methods=['GET'])
def get_inspections(portfolio_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM property_inspections WHERE portfolio_id = ? ORDER BY inspection_date DESC', (portfolio_id,))
        inspections = [dict(row) for row in cursor.fetchall()]
        
        # Parse JSON strings
        for insp in inspections:
            insp['data_json'] = json.loads(insp['data_json'])
            insp['score_summary'] = json.loads(insp['score_summary'])
            
        conn.close()
        return jsonify(inspections)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
