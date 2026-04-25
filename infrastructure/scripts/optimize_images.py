import os
import sqlite3
from PIL import Image

# Path configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DB_PATH = os.path.join(BASE_DIR, 'data', 'imza_database.db')

def convert_to_webp(source_path):
    """Converts an image to webp format."""
    try:
        if not source_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            return None
        
        target_path = os.path.splitext(source_path)[0] + '.webp'
        
        # Don't re-convert if already exists
        if os.path.exists(target_path):
            return target_path
            
        with Image.open(source_path) as img:
            img.save(target_path, 'WEBP', quality=80)
            print(f"Converted: {os.path.basename(source_path)} -> {os.path.basename(target_path)}")
            return target_path
    except Exception as e:
        print(f"Error converting {source_path}: {e}")
        return None

def update_db_references(old_rel_path, new_rel_path):
    """Updates the database path references for portfolios."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Update main portfolio images
        cursor.execute("UPDATE portfoyler SET resim_hero = ? WHERE resim_hero = ?", (new_rel_path, old_rel_path))
        cursor.execute("UPDATE portfoyler SET resim_hikaye = ? WHERE resim_hikaye = ?", (new_rel_path, old_rel_path))
        
        # Update portfolio media gallery
        cursor.execute("UPDATE portfoy_medya SET file_path = ? WHERE file_path = ?", (new_rel_path, old_rel_path))
        cursor.execute("UPDATE portfoy_medya SET local_path = ? WHERE local_path = ?", (new_rel_path, old_rel_path))
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database update error: {e}")

def optimize_all():
    print("Starting WebP Optimization...")
    count = 0
    if not os.path.exists(UPLOAD_FOLDER):
        print(f"Upload folder not found: {UPLOAD_FOLDER}")
        return

    for root, dirs, files in os.walk(UPLOAD_FOLDER):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                webp_path = convert_to_webp(full_path)
                
                if webp_path:
                    # Calculate relative paths for DB update
                    # /uploads/filename.jpg -> /uploads/filename.webp
                    rel_old = os.path.join('/uploads', os.path.relpath(full_path, UPLOAD_FOLDER)).replace('\\', '/')
                    rel_new = os.path.join('/uploads', os.path.relpath(webp_path, UPLOAD_FOLDER)).replace('\\', '/')
                    
                    update_db_references(rel_old, rel_new)
                    count += 1

    print(f"Optimization complete. {count} images processed.")

if __name__ == "__main__":
    optimize_all()
