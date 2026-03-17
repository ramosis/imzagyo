import shutil
import os
import time
from datetime import datetime

# Yapılandırma
DB_PATH = 'data/imza.db'
BACKUP_DIR = 'data/backups'
MAX_BACKUPS = 7  # Son 7 yedeği tut

def backup_database():
    if not os.path.exists(DB_PATH):
        print(f"Hata: {DB_PATH} bulunamadı.")
        return

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = os.path.join(BACKUP_DIR, f'imza_backup_{timestamp}.db')

    try:
        shutil.copy2(DB_PATH, backup_file)
        print(f"Yedekleme başarılı: {backup_file}")
        cleanup_old_backups()
    except Exception as e:
        print(f"Yedekleme sırasında hata oluştu: {e}")

def cleanup_old_backups():
    backups = [os.path.join(BACKUP_DIR, f) for f in os.listdir(BACKUP_DIR) if f.endswith('.db')]
    backups.sort(key=os.path.getmtime)

    while len(backups) > MAX_BACKUPS:
        oldest_backup = backups.pop(0)
        os.remove(oldest_backup)
        print(f"Eski yedek silindi: {oldest_backup}")

if __name__ == '__main__':
    backup_database()
