import sqlite3
from flask import Blueprint, jsonify, request
from database import DB_NAME

hero_bp = Blueprint('hero', __name__)

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@hero_bp.route('/api/hero', methods=['GET'])
def get_slides():
    conn = get_db_connection()
    slides = conn.execute('SELECT * FROM hero_slides ORDER BY sira ASC').fetchall()
    conn.close()
    return jsonify([dict(s) for s in slides])

@hero_bp.route('/api/hero/<int:slide_id>', methods=['GET'])
def get_slide(slide_id):
    conn = get_db_connection()
    slide = conn.execute('SELECT * FROM hero_slides WHERE id = ?', (slide_id,)).fetchone()
    conn.close()
    if slide is None:
        return jsonify({"error": "Slide bulunamadı"}), 404
    return jsonify(dict(slide))

@hero_bp.route('/api/hero', methods=['POST'])
def add_slide():
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO hero_slides 
            (resim_url, alt_baslik, baslik_satir1, baslik_satir2, buton1_metin, buton2_metin, buton2_link, sira)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('resim_url', ''),
            data.get('alt_baslik', ''),
            data.get('baslik_satir1', ''),
            data.get('baslik_satir2', ''),
            data.get('buton1_metin', ''),
            data.get('buton2_metin', ''),
            data.get('buton2_link', ''),
            data.get('sira', 0)
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Slide başarıyla eklendi."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@hero_bp.route('/api/hero/<int:slide_id>', methods=['PUT'])
def update_slide(slide_id):
    data = request.json
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE hero_slides SET 
                resim_url = ?, 
                alt_baslik = ?, 
                baslik_satir1 = ?, 
                baslik_satir2 = ?, 
                buton1_metin = ?, 
                buton2_metin = ?, 
                buton2_link = ?, 
                sira = ?
            WHERE id = ?
        ''', (
            data.get('resim_url', ''),
            data.get('alt_baslik', ''),
            data.get('baslik_satir1', ''),
            data.get('baslik_satir2', ''),
            data.get('buton1_metin', ''),
            data.get('buton2_metin', ''),
            data.get('buton2_link', ''),
            data.get('sira', 0),
            slide_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Slide güncellendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@hero_bp.route('/api/hero/<int:slide_id>', methods=['DELETE'])
def delete_slide(slide_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM hero_slides WHERE id = ?', (slide_id,))
        conn.commit()
        conn.close()
        return jsonify({"success": True, "message": "Slide silindi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
