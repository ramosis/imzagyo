import sqlite3

db = sqlite3.connect('imza_database.db')
cur = db.cursor()

try:
    # Taraflar tablosunda test verisi var mı kontrol et, yoksa 1 tane alıcı ve satıcı ekle 
    cur.execute("SELECT COUNT(*) FROM parties")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("INSERT INTO parties (tc_no, party_type, name, phone, email) VALUES ('12345678901', 'individual', 'Ahmet Yılmaz', '5551234567', 'ahmet@example.com')")
        cur.execute("INSERT INTO parties (vkn, party_type, name, phone, email) VALUES ('9876543210', 'corporate', 'Yılmazlar İnşaat', '5559876543', 'info@yilmazlar.com')")
        db.commit()
        print("Taraf test verisi eklendi.")
    else:
        print(f"Taraflar tablosunda {count} kayıt var.")
except Exception as e:
    print(f"Hata: {e}")

db.close()
