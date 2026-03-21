import os
from flask import Blueprint, request, jsonify, current_app
from database import get_db_connection
from api.upload_service import upload_image_to_cloudinary
from werkzeug.utils import secure_filename

media_bp = Blueprint('media', __name__)

# Helper to check allowed extensions (reuse from app.py)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@media_bp.route('/api/media', methods=['POST'])
def upload_media():
    """Upload a media file for a portfolio item.
    Expected form-data fields:
        - portfolio_id: ID of the portfolio (portfoyler.id)
        - category: one of ['İç Mekan', 'Dış Mekan', 'Drone', 'Video', 'Plan']
        - file: the image/video file
    Returns JSON with media record ID and URLs.
    """
    portfolio_id = request.form.get('portfolio_id')
    category = request.form.get('category')
    file = request.files.get('file')
    
    if not portfolio_id or not category or not file:
        return jsonify({'error': 'Missing required fields'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
        
    filename = secure_filename(file.filename)
    
    # 1. Kategori bazlı alt klasör belirle
    category_map = {
        'İç Mekan': 'photos',
        'Dış Mekan': 'photos',
        'Drone': 'drone',
        'Video': 'vids',
        'Plan': 'plans',
        'Belge': 'docs'
    }
    subdir = category_map.get(category, 'others')
    
    # 2. Klasör Yapısını Oluştur: uploads/properties/{id}/{subdir}/
    prop_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'properties', str(portfolio_id), subdir)
    os.makedirs(prop_folder, exist_ok=True)
    
    # 3. Dosyayı Kalıcı Olarak Kaydet
    # Çakışmayı önlemek için timestamp ekle
    import time
    safe_filename = f"{int(time.time())}_{filename}"
    local_path = os.path.join(prop_folder, safe_filename)
    file.save(local_path)
    
    # 4. Buluta (Cloudinary) Yükle (Yedek ve CDN için)
    # Not: Bazı belgeler (sözleşme vb.) sadece yerelde kalabilir, ama şimdilik her şeyi yüklüyoruz.
    upload_res = upload_image_to_cloudinary(local_path)
    
    if not upload_res.get('success'):
        # Cloudinary başarısız olsa bile yerel dosya duruyor, devam edebiliriz 
        # veya hata dönebiliriz. Kullanıcı "sunucu içi" istediği için devam ediyoruz.
        cloudinary_url = ""
    else:
        cloudinary_url = upload_res['url']
        
    # Veritabanı Yolu (Göreli Yol)
    relative_local_path = os.path.relpath(local_path, current_app.root_path)
        
    # 5. Veritabanına Kaydet
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO portfoy_medya (portfolio_id, category, file_path, local_path)
        VALUES (?,?,?,?)
    ''', (portfolio_id, category, cloudinary_url or relative_local_path, relative_local_path))
    
    media_id = cur.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({
        'status': 'created', 
        'media_id': media_id, 
        'url': cloudinary_url or f"/{relative_local_path.replace(os.sep, '/')}",
        'local_path': relative_local_path
    }), 201

@media_bp.route('/api/media/<int:media_id>', methods=['PATCH'])
def update_media_meta(media_id):
    """Update metadata such as focal point coordinates.
    Expected JSON body: {"focal_x": float, "focal_y": float}
    """
    data = request.get_json() or {}
    focal_x = data.get('focal_x')
    focal_y = data.get('focal_y')
    
    if focal_x is None or focal_y is None:
        return jsonify({'error': 'Missing focal coordinates'}), 400
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        UPDATE portfoy_medya SET focal_x = ?, focal_y = ? WHERE id = ?
    ''', (focal_x, focal_y, media_id))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'updated'}), 200

@media_bp.route('/api/media/portfolio/<portfolio_id>', methods=['GET'])
def list_media_for_portfolio(portfolio_id):
    """Get all media for a specific portfolio item."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM portfoy_medya WHERE portfolio_id = ? ORDER BY category, id', (portfolio_id,))
    rows = cur.fetchall()
    conn.close()
    
    media = [dict(row) for row in rows]
    return jsonify(media), 200

@media_bp.route('/api/media/<int:media_id>', methods=['DELETE'])
def delete_media(media_id):
    """Delete a media record."""
    # Note: Should ideally also delete from Cloudinary here
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM portfoy_medya WHERE id = ?', (media_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'deleted'}), 200
