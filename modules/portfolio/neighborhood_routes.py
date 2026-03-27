import urllib.request
import re
import os
import threading
from datetime import datetime
from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_permission, login_required, require_inner_circle
from . import portfolio_bp

# Business Listings (Esnaf)
@portfolio_bp.route('/neighborhoods/businesses', methods=['GET'])
def get_businesses():
    category = request.args.get('category')
    approved_only = request.args.get('approved_only', 'true').lower() == 'true'
    with get_db() as conn:
        query = 'SELECT * FROM businesses WHERE 1=1'
        params = []
        if approved_only: query += ' AND is_approved = 1'
        if category:
            query += ' AND category = ?'
            params.append(category)
        query += ' ORDER BY rating DESC, name ASC'
        businesses = conn.execute(query, params).fetchall()
    return jsonify([dict(b) for b in businesses]), 200

@portfolio_bp.route('/neighborhoods/businesses/<int:id>', methods=['GET'])
def get_business(id):
    with get_db() as conn:
        business = conn.execute('SELECT * FROM businesses WHERE id = ?', (id,)).fetchone()
    if business is None:
        return jsonify({'error': 'Business not found'}), 404
    return jsonify(dict(business)), 200

@portfolio_bp.route('/neighborhoods/businesses', methods=['POST'])
@require_inner_circle
def add_business():
    data = request.json
    if not data or not data.get('name') or not data.get('category'):
        return jsonify({'error': 'Name and category are required'}), 400
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO businesses (name, category, description, phone, address, logo_url, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['category'], data.get('description'), data.get('phone'), 
              data.get('address'), data.get('logo_url'), data.get('is_approved', True)))
        conn.commit()
    return jsonify({'status': 'created'}), 201

# Pharmacy Scraper
@portfolio_bp.route('/neighborhoods/pharmacies/duty', methods=['GET'])
def get_duty_pharmacies():
    try:
        url = "https://www.kutahyaeo.org.tr/nobetci-eczaneler/30"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')
        pharmacies = []
        matches = re.finditer(r'<h4[^>]*>(.*?)</h4>(.*?)(?=<h4|$)', html, re.DOTALL | re.IGNORECASE)
        for match in matches:
            name_raw = match.group(1).strip()
            if "Çerez" in name_raw or "OBEN" in name_raw: continue
            block = match.group(2)
            phone_match = re.search(r'href=["\']tel:([^"\']+)["\']', block, re.IGNORECASE)
            phone = phone_match.group(1).strip() if phone_match else ""
            addr_text = re.sub(r'<[^>]+>', ' ', block).strip()
            if phone: addr_text = addr_text.replace(phone, '').strip()
            addr_text = re.sub(r'\s+', ' ', addr_text).replace("Haritada görüntülemek için tıklayınız...", "").strip()
            if name_raw: pharmacies.append({"name": name_raw, "address": addr_text, "phone": phone, "is_duty": True})
        return jsonify({"status": "success", "date": datetime.now().strftime("%Y-%m-%d"), "data": pharmacies}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Hata: {str(e)}", "data": []}), 500

# Unit & Expense Management
@portfolio_bp.route('/neighborhoods/my-unit', methods=['GET'])
@login_required
def get_my_unit():
    unit_id = request.args.get('unit_id', type=int)
    if not unit_id: return jsonify({"error": "unit_id required"}), 400
    with get_db() as conn:
        unit = conn.execute('SELECT * FROM property_units WHERE id = ?', (unit_id,)).fetchone()
        dues = conn.execute('SELECT * FROM dues_payments WHERE unit_id = ? ORDER BY period DESC', (unit_id,)).fetchall()
    if not unit: return jsonify({"error": "Unit not found"}), 404
    return jsonify({'unit': dict(unit), 'payments': [dict(d) for d in dues]}), 200

@portfolio_bp.route('/neighborhoods/cashbox/<property_id>', methods=['GET'])
@login_required
def get_transparent_cashbox(property_id):
    with get_db() as conn:
        incomes = conn.execute('''
            SELECT d.payment_type, SUM(d.amount) as total FROM dues_payments d
            JOIN property_units pu ON d.property_unit_id = pu.id
            WHERE pu.property_id = ? AND d.status = 'Ödendi' GROUP BY d.payment_type
        ''', (property_id,)).fetchall()
        total_income = sum([row['total'] for row in incomes]) if incomes else 0
        expenses = conn.execute('''
            SELECT expense_type, SUM(amount) as total FROM apartment_expenses
            WHERE property_id = ? GROUP BY expense_type
        ''', (property_id,)).fetchall()
        total_expense = sum([row['total'] for row in expenses]) if expenses else 0
    return jsonify({
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': total_income - total_expense,
        'income_breakdown': [dict(i) for i in incomes],
        'expense_breakdown': [dict(e) for e in expenses]
    }), 200

# Social Wall
@portfolio_bp.route('/neighborhoods/posts', methods=['GET'])
def get_wall_posts():
    post_type = request.args.get('type')
    limit = request.args.get('limit', 20)
    with get_db() as conn:
        query = '''
            SELECT p.*, u.username, u.role FROM neighborhood_posts p
            LEFT JOIN users u ON p.user_id = u.id WHERE 1=1
        '''
        params = []
        if post_type:
            query += ' AND p.type = ?'
            params.append(post_type)
        query += ' ORDER BY p.created_at DESC LIMIT ?'
        params.append(limit)
        posts = conn.execute(query, params).fetchall()
    return jsonify([dict(p) for p in posts]), 200

@portfolio_bp.route('/neighborhoods/posts', methods=['POST'])
@login_required
def create_wall_post():
    data = request.json
    content = data.get('content')
    post_type = data.get('type')
    allowed_types = ['ulasim', 'paylasim', 'yardim', 'duyuru']
    if not content or post_type not in allowed_types:
        return jsonify({'error': 'Invalid content or type'}), 400
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO neighborhood_posts (user_id, type, content, image_url) VALUES (?, ?, ?, ?)', 
                    (g.user['id'], post_type, content, data.get('image_url')))
        conn.commit()
    return jsonify({'status': 'created'}), 201
