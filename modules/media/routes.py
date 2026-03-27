from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import login_required
from . import media_bp
from .service import process_and_save_media

@media_bp.route('/portfolio/<portfolio_id>', methods=['GET'])
def list_portfolio_media(portfolio_id):
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM portfoy_medya WHERE portfolio_id = ? ORDER BY category, id', (portfolio_id,)).fetchall()
    return jsonify([dict(row) for row in rows])

@media_bp.route('/', methods=['POST'])
@login_required
def upload_portfolio_media():
    portfolio_id = request.form.get('portfolio_id')
    category = request.form.get('category')
    file = request.files.get('file')
    if not all([portfolio_id, category, file]): return jsonify({'error': 'Missing fields'}), 400
    
    result = process_and_save_media(file, portfolio_id, category)
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO portfoy_medya (portfolio_id, category, file_path, local_path) VALUES (?,?,?,?)',
                    (portfolio_id, category, result['url'], result['local_path']))
        media_id = cur.lastrowid
        conn.commit()
    return jsonify({'id': media_id, 'url': result['url']}), 201

@media_bp.route('/<int:media_id>', methods=['DELETE'])
@login_required
def delete_media(media_id):
    with get_db() as conn:
        conn.execute('DELETE FROM portfoy_medya WHERE id = ?', (media_id,))
        conn.commit()
    return jsonify({'status': 'deleted'}), 200
