import sqlite3
import time
import datetime
import os
import requests

# Get database path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "data", "imza_database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def run_automations():
    """Aktif otomasyon kurallarını denetler ve çalıştırır."""
    print(f"[{datetime.datetime.now()}] Otomasyon denetimi başlatıldı...")
    conn = get_db_connection()
    rules = conn.execute("SELECT * FROM automations WHERE is_active = 1").fetchall()
    
    for rule in rules:
        # Örnek Mantık: Eğer tetikleyici 'New Lead' ise ve son 1 saatte yeni lead geldiyse
        if rule['trigger_event'] == 'new_lead':
            # Son kontrol zamanından beri yeni lead var mı bak
            leads = conn.execute("SELECT * FROM leads WHERE created_at > datetime('now', '-1 hour')").fetchall()
            for lead in leads:
                print(f"-> Kural Çalışıyor: {rule['name']} | Hedef: {lead['name']}")
                # Burada Aksiyon Alınır (E-posta gönderimi vb.)
                # requests.post(...) 
                
        # Kuralın son çalışma zamanını güncelle
        conn.execute("UPDATE automations SET last_run = CURRENT_TIMESTAMP WHERE id = ?", (rule['id'],))
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    print("İmza Gayrimenkul Otomasyon Scheduler Başlatıldı.")
    while True:
        try:
            run_automations()
        except Exception as e:
            print(f"HATA: {e}")
        
        # Her 1 saatte bir çalış (veya test için shorter)
        time.sleep(3600) 
