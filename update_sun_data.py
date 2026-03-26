import sqlite3

DB_NAME = "data/imza_database.db"

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
