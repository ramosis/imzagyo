from flask import Blueprint, jsonify, request
import sqlite3
import os

lmetrics_bp = Blueprint('lmetrics', __name__)

DB_NAME = 'imza_emlak.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@lmetrics_bp.route('/api/lmetrics/collect', methods=['POST'])
def collect_interaction():
    """Kullanıcı etkileşim verilerini toplar."""
    data = request.json
    session_id = data.get('session_id')
    url = data.get('url')
    event_type = data.get('event_type')
    element_id = data.get('element_id')
    value = data.get('value')

    if not all([session_id, event_type]):
        return jsonify({"error": "session_id ve event_type zorunludur"}), 400

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO user_interactions (session_id, url, event_type, element_id, value)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, url, event_type, element_id, value))
    conn.commit()
    conn.close()

    return jsonify({"status": "success"}), 201

@lmetrics_bp.route('/api/lmetrics/stats/<session_id>', methods=['GET'])
def get_user_stats(session_id):
    """Belirli bir session için etkileşim özetini getirir."""
    conn = get_db_connection()
    stats = conn.execute('''
        SELECT event_type, COUNT(*) as count 
        FROM user_interactions 
        WHERE session_id = ? 
        GROUP BY event_type
    ''', (session_id,)).fetchall()
    
    # Niyet Skoru Hesaplama (Basit Örnek)
    # Tıklama, derin scroll ve uzun süre kalma skoru artırır.
    score = 0
    for s in stats:
        if s['event_type'] == 'click': score += s['count'] * 10
        if s['event_type'] == 'scroll' and int(s['count']) > 5: score += 20
        if s['event_type'] == 'stay': score += s['count'] * 5

    conn.close()
    return jsonify({
        "session_id": session_id,
        "stats": [dict(s) for s in stats],
        "intent_score": min(score, 100) # Max 100
    }), 200
