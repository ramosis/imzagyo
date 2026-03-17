from flask import Blueprint, request, jsonify
from database import get_db_connection
import json

tracking_bp = Blueprint('tracking', __name__)

@tracking_bp.route('/api/track', methods=['POST'])
def track_event():
    data = request.json
    session_id = data.get('session_id')
    event_type = data.get('event_type') # 'page_view', 'tool_usage', 'click'
    page_url = data.get('page_url')
    meta_data = data.get('meta_data', {})
    
    if not session_id:
        return jsonify({'status': 'ignored'}), 200

    conn = get_db_connection()
    try:
        # Etkileşimi kaydet
        conn.execute('''
            INSERT INTO lead_interactions (session_id, tool_name, data_json)
            VALUES (?, ?, ?)
        ''', (session_id, event_type, json.dumps({'url': page_url, 'meta': meta_data})))
        conn.commit()
        return jsonify({'status': 'tracked'}), 201
    finally:
        conn.close()

@tracking_bp.route('/api/tracking/sync', methods=['POST'])
def sync_metrics():
    data = request.json
    shadow_id = data.get('shadow_id')
    metrics = data.get('metrics', {})
    geo = data.get('geo', {})
    
    if not shadow_id:
        return jsonify({'error': 'Missing shadow_id'}), 400

    conn = get_db_connection()
    try:
        # Ziyaretçi senkronizasyonu (JSON formatında saklama)
        conn.execute('''
            INSERT INTO lead_interactions (session_id, tool_name, data_json)
            VALUES (?, ?, ?)
        ''', (shadow_id, 'L-Metrics Sync', json.dumps({
            'metrics': metrics,
            'geo': geo,
            'url': request.referrer
        })))
        conn.commit()
        return jsonify({'status': 'synced'}), 201
    finally:
        conn.close()