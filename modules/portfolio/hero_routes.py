from flask import request, jsonify
from shared.schemas import heros_schema
from modules.auth.decorators import require_permission
from . import portfolio_bp
from .repository import HeroRepository

@portfolio_bp.route('/hero', methods=['GET'])
def get_slides():
    rows = HeroRepository.get_all()
    return jsonify(heros_schema.dump(rows))

@portfolio_bp.route('/hero/<int:slide_id>', methods=['GET'])
def get_slide(slide_id):
    slide = HeroRepository.get_by_id(slide_id)
    if slide is None:
        return jsonify({"error": "Slide bulunamadı"}), 404
    return jsonify(slide)

@portfolio_bp.route('/hero', methods=['POST'])
@require_permission('admin')
def add_slide():
    try:
        data = request.json
        HeroRepository.create(data)
        return jsonify({"success": True, "message": "Slide başarıyla eklendi."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@portfolio_bp.route('/hero/<int:slide_id>', methods=['PUT'])
@require_permission('admin')
def update_slide(slide_id):
    try:
        data = request.json
        if HeroRepository.update(slide_id, data):
            return jsonify({"success": True, "message": "Slide güncellendi."})
        return jsonify({"error": "Slide bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@portfolio_bp.route('/hero/<int:slide_id>', methods=['DELETE'])
@require_permission('admin')
def delete_slide(slide_id):
    try:
        if HeroRepository.delete(slide_id):
            return jsonify({"success": True, "message": "Slide silindi."})
        return jsonify({"error": "Slide bulunamadı"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
