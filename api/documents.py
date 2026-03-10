from flask import Blueprint, request, jsonify, current_app
from database import get_db_connection
import os
import time
from werkzeug.utils import secure_filename

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/api/documents', methods=['GET'])
def get_documents():
    conn = get_db_connection()
    docs = conn.execute('SELECT * FROM incoming_docs ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in docs])

@documents_bp.route('/api/documents', methods=['POST'])
def add_document():
    # Form verilerini al
    sender = request.form.get('sender')
    source = request.form.get('source')
    content = request.form.get('content')
    file = request.files.get('file')
    
    file_path = None
    file_type = 'text'
    
    if file:
        filename = secure_filename(file.filename)
        # Klasör yoksa oluştur
        upload_dir = os.path.join(current_app.root_path, 'uploads', 'documents')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Benzersiz isim ver
        safe_filename = f"{int(time.time())}_{filename}"
        save_path = os.path.join(upload_dir, safe_filename)
        file.save(save_path)
        
        file_path = f"/uploads/documents/{safe_filename}"
        
        # Dosya tipini belirle
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            file_type = 'image'
        elif ext == 'pdf':
            file_type = 'pdf'
        else:
            file_type = 'file'

    conn = get_db_connection()
    conn.execute('''
        INSERT INTO incoming_docs (source, sender, file_path, file_type, content, status)
        VALUES (?, ?, ?, ?, ?, 'new')
    ''', (source, sender, file_path, file_type, content))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success'}), 201

@documents_bp.route('/api/documents/<int:id>/status', methods=['PUT'])
def update_status(id):
    data = request.json
    conn = get_db_connection()
    conn.execute('UPDATE incoming_docs SET status = ? WHERE id = ?', (data.get('status'), id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'updated'})

@documents_bp.route('/api/documents/<int:id>', methods=['DELETE'])
def delete_document(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM incoming_docs WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'deleted'})