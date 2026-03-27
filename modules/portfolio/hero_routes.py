from flask import request, jsonify
from shared.database import get_db
from shared.schemas import heros_schema
from modules.auth.decorators import require_permission
from . import portfolio_bp

@portfolio_bp.route('/hero', methods=['GET'])
def get_slides():
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM hero_slides ORDER BY sira ASC').fetchall()
    return jsonify(heros_schema.dump([dict(r) for r in rows]))

@portfolio_bp.route('/hero/<int:slide_id>', methods=['GET'])
def get_slide(slide_id):
    with get_db() as conn:
        slide = conn.execute('SELECT * FROM hero_slides WHERE id = ?', (slide_id,)).fetchone()
    if slide is None:
        return jsonify({"error": "Slide bulunamadı"}), 404
    return jsonify(dict(slide))

@portfolio_bp.route('/hero', methods=['POST'])
@require_permission('admin')
def add_slide():
    data = request.json
    try:
        with get_db() as conn:
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
        return jsonify({"success": True, "message": "Slide başarıyla eklendi."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@portfolio_bp.route('/hero/<int:slide_id>', methods=['PUT'])
@require_permission('admin')
def update_slide(slide_id):
    data = request.json
    try:
        with get_db() as conn:
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
        return jsonify({"success": True, "message": "Slide güncellendi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@portfolio_bp.route('/hero/<int:slide_id>', methods=['DELETE'])
@require_permission('admin')
def delete_slide(slide_id):
    try:
        with get_db() as conn:
            conn.execute('DELETE FROM hero_slides WHERE id = ?', (slide_id,))
            conn.commit()
        return jsonify({"success": True, "message": "Slide silindi."})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
