import os
import time
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

import filetype

# Helper to check allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf', 'docx', 'doc', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_safe_file_content(file_stream) -> bool:
    """Uses magic bytes (filetype) to ensure file matches allowed types."""
    # Read the first 2Kb to guess file type
    header = file_stream.read(2048)
    file_stream.seek(0)
    
    kind = filetype.guess(header)
    
    # Generic check for standard extensions
    if kind and kind.extension in ALLOWED_EXTENSIONS:
        return True
        
    # Extra check for Office files which might be detected as zip/ole
    office_mimes = [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'application/msword',
        'application/vnd.ms-excel'
    ]
    if kind and kind.mime in office_mimes:
        return True
        
    return False

def upload_to_cloudinary(file_path, folder="imza_gayrimenkul"):
    """Yerel dosyayı Cloudinary'ye yükler."""
    try:
        upload_result = cloudinary.uploader.upload(
            file_path, folder=folder, use_filename=True,
            unique_filename=True, overwrite=False, resource_type="auto"
        )
        return {"success": True, "url": upload_result.get("secure_url"), "public_id": upload_result.get("public_id")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def process_and_save_media(file, portfolio_id, category):
    """Görseli optimize eder ve hem yerel hem buluta kaydeder."""
    if not is_safe_file_content(file):
        raise ValueError("Invalid file content or signature")
        
    import uuid
    # Enforce uuid-based unique filename to avoid path traversal / spoofing
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'bin'
    filename = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    category_map = {
        'İç Mekan': 'photos', 'Dış Mekan': 'photos', 'Drone': 'drone',
        'Video': 'vids', 'Plan': 'plans', 'Belge': 'docs'
    }
    subdir = category_map.get(category, 'others')
    prop_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], 'properties', str(portfolio_id), subdir)
    os.makedirs(prop_folder, exist_ok=True)
    
    safe_filename = f"{int(time.time())}_{filename}"
    local_path = os.path.join(prop_folder, safe_filename)
    
    is_image = category in ['İç Mekan', 'Dış Mekan', 'Drone', 'Plan']
    if is_image:
        try:
            img = Image.open(file)
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
            if img.width > 1920:
                ratio = 1920 / float(img.width)
                img = img.resize((1920, int(img.height * ratio)), Image.Resampling.LANCZOS)
            img.save(local_path, format='JPEG', quality=85, optimize=True)
        except:
            file.seek(0); file.save(local_path)
    else:
        file.save(local_path)
    
    upload_res = upload_to_cloudinary(local_path)
    relative_path = os.path.relpath(local_path, current_app.root_path)
    return {
        "local_path": relative_path,
        "url": upload_res.get('url', f"/{relative_path.replace(os.sep, '/')}")
    }
