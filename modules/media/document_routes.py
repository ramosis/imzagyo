import os, time
from flask import request, jsonify, current_app
from shared.database import get_db
from modules.auth.decorators import login_required
from werkzeug.utils import secure_filename
from . import media_bp

@media_bp.route('/documents', methods=['GET'])
@login_required
def get_documents():
    with get_db() as conn:
        docs = conn.execute('SELECT * FROM incoming_docs ORDER BY created_at DESC').fetchall()
    return jsonify([dict(row) for row in docs])

@media_bp.route('/documents', methods=['POST'])
@login_required
def add_document():
    sender = request.form.get('sender')
    source = request.form.get('source')
    content = request.form.get('content')
    file = request.files.get('file')
    
    file_path = None
    file_type = 'text'
    if file:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join(current_app.root_path, 'uploads', 'documents')
        os.makedirs(upload_dir, exist_ok=True)
        safe_filename = f"{int(time.time())}_{filename}"
        save_path = os.path.join(upload_dir, safe_filename)
        file.save(save_path)
        file_path = f"/uploads/documents/{safe_filename}"
        
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        if ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']: file_type = 'image'
        elif ext == 'pdf': file_type = 'pdf'
        else: file_type = 'file'

    with get_db() as conn:
        conn.execute('INSERT INTO incoming_docs (source, sender, file_path, file_type, content, status) VALUES (?,?,?,?,?,?)',
                     (source, sender, file_path, file_type, content, 'new'))
        conn.commit()
    return jsonify({'status': 'success'}), 201
