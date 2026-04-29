from . import ai_bp
from flask import Blueprint, request, jsonify
from backend.app.extensions import limiter
from .service import AIService

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/v1/ai/chat', methods=['POST'])
@limiter.limit("10 per minute")
def ai_chat():
    data = request.json
    message = data.get('message')
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    response = AIService.get_response(message)
    return jsonify({'response': response}), 200

@ai_bp.route('/api/v1/ai/translate', methods=['POST'])
def ai_translate():
    data = request.json
    text = data.get('text')
    target_lang = data.get('target_lang', 'en')
    if not text:
        return jsonify({'error': 'Text is required'}), 400
        
    translated = AIService.translate_text(text, target_lang)
    return jsonify({'translated': translated}), 200
