import sqlite3
import os

# Get database path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_NAME = os.path.join(BASE_DIR, "data", "imza_database.db")

def update_sample_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Boğaz Manzaralı Villa için örnek güneş verisi
    cursor.execute('''
        UPDATE portfoyler 
        SET cephe = 'Güney', 
            gunes_bilgisi = 'Bu villa tam Güney cepheli olup, sabah güneş doğuşundan akşam batışına kadar kesintisiz direkt ışık almaktadır. Kış aylarında bile doğal ısınma avantajı sağlar.' 
        WHERE id = 'bogaz-villa'
    ''')
    
    conn.commit()
    conn.close()
    print("Örnek portföy 'bogaz-villa' güneş verileriyle güncellendi.")

if __name__ == "__main__":
    update_sample_data()
