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
    
    try:
        result = process_and_save_media(file, portfolio_id, category)
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
        
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

@media_bp.route('/vault', methods=['GET'])
@login_required
def get_media_vault():
    # Placeholder: In a real app this would query a 'general_media' table
    # For now, we list files in the uploads/general directory if it exists
    import os
    from flask import current_app
    vault_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'general')
    if not os.path.exists(vault_path):
        return jsonify([]), 200
        
    files = []
    for f in os.listdir(vault_path):
        files.append({
            'name': f,
            'url': f'/uploads/general/{f}',
            'type': f.split('.')[-1] if '.' in f else 'file'
        })
    return jsonify(files), 200
@media_bp.route('/vault/<filename>', methods=['DELETE'])
@login_required
def delete_vault_media(filename):
    import os
    from flask import current_app
    # Security: check if moving out of general folder is prevented
    if '..' in filename or filename.startswith('/'):
        return jsonify({'error': 'Geçersiz dosya adı'}), 400
        
    vault_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'general', filename)
    if os.path.exists(vault_path):
        try:
            os.remove(vault_path)
            return jsonify({'message': 'Dosya başarıyla silindi'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'Dosya bulunamadı'}), 404
