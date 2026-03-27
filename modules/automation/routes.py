import json
from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import automation_bp

@automation_bp.route('/rules', methods=['GET'])
@require_inner_circle
def get_rules():
    with get_db() as conn:
        rules = conn.execute('SELECT * FROM automation_rules ORDER BY created_at DESC').fetchall()
    return jsonify([dict(r) for r in rules])

@automation_bp.route('/rules', methods=['POST'])
@require_inner_circle
def create_rule():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO automation_rules (name, trigger_type, condition_json, action_type, action_template_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (data.get('name'), data.get('trigger_type'), json.dumps(data.get('condition', {})), 
              data.get('action_type', 'email'), data.get('action_template_id')))
        conn.commit()
    return jsonify({'status': 'success'}), 201

# Campaigns (formerly campaigns.py)
@automation_bp.route('/campaigns', methods=['GET'])
@require_inner_circle
def get_campaigns():
    with get_db() as conn:
        campaigns = conn.execute('SELECT * FROM campaigns').fetchall()
    return jsonify([dict(c) for c in campaigns])

@automation_bp.route('/campaigns', methods=['POST'])
@require_inner_circle
def add_campaign():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO campaigns (name, target_audience, start_date, end_date, budget, status) VALUES (?,?,?,?,?,?)',
                    (data.get('name'), data.get('target_audience'), data.get('start_date'), 
                     data.get('end_date'), data.get('budget'), data.get('status', 'draft')))
        conn.commit()
    return jsonify({'status': 'created'}), 201
