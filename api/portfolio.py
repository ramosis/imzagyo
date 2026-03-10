import uuid
from flask import Blueprint, request, jsonify, g
from database import get_db_connection
import json

portfolio_bp = Blueprint('portfolio', __name__)

# Simple admin check (placeholder)
def admin_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or (not token.startswith('Bearer token-') and token != 'Bearer admin-token' and token != 'Bearer imza-super-admin-2026'):
            return jsonify({'error': 'Unauthorized'}), 403
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@portfolio_bp.route('/api/portfoyler', methods=['POST'])
@admin_required
def add_portfolio():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Yeni eklendiği için random ID oluşturuyoruz. 
    # Frontend'de id boş string veya null gelirse.
    new_id = data.get('id')
    if not new_id:
        new_id = str(uuid.uuid4())

    cur.execute('''
        INSERT INTO portfoyler (id, koleksiyon, baslik1, baslik2, lokasyon, refNo, fiyat, oda, alan, kat, isitma, ozellik_renk, bg_renk, btn_renk, icon_renk, resim_hero, resim_hikaye, hikaye, ozellikler, ozellik_kategori, mulk_tipi)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    ''', (
        new_id, data.get('koleksiyon'), data.get('baslik1'), data.get('baslik2'), data.get('lokasyon'), data.get('refNo'), data.get('fiyat'), data.get('oda'), data.get('alan'), data.get('kat'), data.get('isitma'), data.get('ozellik_renk', 'bg-navy text-gold'), data.get('bg_renk'), data.get('btn_renk'), data.get('icon_renk'), data.get('resim_hero'), data.get('resim_hikaye'), data.get('hikaye'), json.dumps(data.get('ozellikler_arr', [])), data.get('ozellik_kategori'), data.get('mulk_tipi', 'Konut')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'created', 'id': new_id}), 201

@portfolio_bp.route('/api/portfoyler/<id>', methods=['PUT'])
@admin_required
def update_portfolio(id):
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE portfoyler SET koleksiyon=?, baslik1=?, baslik2=?, lokasyon=?, refNo=?, fiyat=?, oda=?, alan=?, kat=?, isitma=?, ozellik_renk=?, resim_hero=?, resim_hikaye=?, hikaye=?, ozellikler=?, ozellik_kategori=?, mulk_tipi=? WHERE id=?
    ''', (
        data.get('koleksiyon'), data.get('baslik1'), data.get('baslik2'), data.get('lokasyon'), data.get('refNo'), data.get('fiyat'), data.get('oda'), data.get('alan'), data.get('kat'), data.get('isitma'), data.get('ozellik_renk', 'bg-navy text-gold'), data.get('resim_hero'), data.get('resim_hikaye'), data.get('hikaye'), json.dumps(data.get('ozellikler_arr', [])), data.get('ozellik_kategori'), data.get('mulk_tipi', 'Konut'), id
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'}), 200

@portfolio_bp.route('/api/portfoyler/<id>', methods=['DELETE'])
@admin_required
def delete_portfolio(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM portfoyler WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'}), 200
