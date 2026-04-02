import sqlite3
import time
import datetime
import os
import requests

# Get project root from modules/core/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_NAME = os.path.join(BASE_DIR, "data", "imza_database.db")

def get_db_connection():
    if not os.path.exists(DB_NAME):
        # Create directory if missing (safety)
        os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def run_automations():
    """Aktif otomasyon kurallarını denetler ve çalıştırır."""
    print(f"[{datetime.datetime.now()}] Otomasyon denetimi başlatıldı...")
    try:
        conn = get_db_connection()
        # Note: Table name might be automation_rules or automations based on modular models
        # Keeping compatibility with current schema for now
        rules = conn.execute("SELECT * FROM automation_rules WHERE is_active = 1").fetchall()
        
        for rule in rules:
            if rule['trigger_event'] == 'new_lead':
                leads = conn.execute("SELECT * FROM leads WHERE created_at > datetime('now', '-1 hour')").fetchall()
                for lead in leads:
                    print(f"-> Kural Çalışıyor: {rule['name']} | Hedef: {lead['name']}")
                    # Action logic here
                    
            conn.execute("UPDATE automation_rules SET last_run = CURRENT_TIMESTAMP WHERE id = ?", (rule['id'],))
            
        conn.commit()
        conn.close()
    except sqlite3.OperationalError as e:
        print(f"UYARI: Otomasyon tablosu henüz hazır değil veya veri yok: {e}")
    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    print("İmza Gayrimenkul Otomasyon Scheduler Başlatıldı (Core Module).")
    while True:
        run_automations()
        # Her 1 saatte bir çalış
        time.sleep(3600) 
