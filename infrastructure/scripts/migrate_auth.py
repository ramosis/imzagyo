import sqlite3
import os

DB_NAME = "imza_database.db"

def migrate():
    if not os.path.exists(DB_NAME):
        print("Veritabanı bulunamadı. Lütfen önce uygulamayı çalıştırın.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Veritabanı güncelleniyor...")

    # 1. users tablosuna email sütunu ekle (eğer yoksa)
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
        print("- users tablosuna email sütunu eklendi.")
    except sqlite3.OperationalError:
        print("- users tablosunda email sütunu zaten mevcut.")

    # 2. password_resets tablosunu oluştur
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL,
            expiry TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    print("- password_resets tablosu oluşturuldu/kontrol edildi.")

    # 3. Örnek admin e-postası ekle
    cursor.execute("UPDATE users SET email = 'admin@imzagayrimenkul.com' WHERE username = 'admin' AND email IS NULL")
    
    conn.commit()
    conn.close()
    print("Güncelleme tamamlandı.")

if __name__ == "__main__":
    migrate()
