from flask import Blueprint, request, jsonify, g
import sqlite3
import json
from shared.database import get_db_connection

mls_bp = Blueprint('mls', __name__)

@mls_bp.route('/api/mls/listings', methods=['POST'])
def share_listing():
    data = request.json
    portfolio_id = data.get('portfolio_id')
    sharing_status = data.get('sharing_status', 'inner') # inner, outer, private
    commission_split = data.get('commission_split', 50.0)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if already exists, then update or insert
        cursor.execute('SELECT id FROM mls_listings WHERE portfolio_id = ?', (portfolio_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE mls_listings SET sharing_status = ?, commission_split = ?
                WHERE portfolio_id = ?
            ''', (sharing_status, commission_split, portfolio_id))
        else:
            cursor.execute('''
                INSERT INTO mls_listings (portfolio_id, sharing_status, commission_split)
                VALUES (?, ?, ?)
            ''', (portfolio_id, sharing_status, commission_split))
            
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Portföy MLS havuzuna başarıyla eklendi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@mls_bp.route('/api/mls/listings', methods=['GET'])
def get_pool():
    # In a real app, we would get the user's role/circle from session/token
    user_circle = request.args.get('circle', 'outer') 

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Inner circle sees everything in inner/outer. Outer circle only sees outer.
        if user_circle == 'inner':
            cursor.execute('''
                SELECT p.*, m.sharing_status, m.commission_split 
                FROM portfoyler p
                JOIN mls_listings m ON p.id = m.portfolio_id
                WHERE m.sharing_status IN ('inner', 'outer')
            ''')
        else:
            cursor.execute('''
                SELECT p.id, p.baslik, p.kategori, p.fiyat, p.lokasyon, m.sharing_status, m.commission_split 
                FROM portfoyler p
                JOIN mls_listings m ON p.id = m.portfolio_id
                WHERE m.sharing_status = 'outer'
            ''')
            
        listings = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(listings)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@mls_bp.route('/api/mls/demands', methods=['POST'])
def add_demand():
    data = request.json
    user_id = data.get('user_id')
    category = data.get('category')
    region = data.get('region')
    budget_max = data.get('budget_max')
    features = json.dumps(data.get('features', {}))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mls_demands (user_id, category, region, budget_max, features_json)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, category, region, budget_max, features))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Talep havuzu güncellendi."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@mls_bp.route('/api/mls/matches', methods=['GET'])
def get_matches():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Simple matching: Region + Category + Budget
        cursor.execute('''
            SELECT d.id as demand_id, p.id as portfolio_id, p.baslik, p.fiyat
            FROM mls_demands d
            JOIN portfoyler p ON d.region = p.lokasyon AND d.category = p.kategori
            JOIN mls_listings m ON p.id = m.portfolio_id
            WHERE d.status = 'open' AND p.fiyat <= d.budget_max
        ''')
        
        matches = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(matches)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
