
import sqlite3
import os

DB_NAME = "imza_database.db"

def update_schema():
    if not os.path.exists(DB_NAME):
        print("Veritabanı bulunamadı.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Sosyal medya ayarları tablosu oluşturuluyor...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS site_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            description TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Varsayılan sosyal medya linklerini ekle
    settings = [
        ('social_facebook', '#', 'Facebook Sayfa Linki'),
        ('social_instagram', '#', 'Instagram Profil Linki'),
        ('social_twitter', '#', 'Twitter Profil Linki'),
        ('social_linkedin', '#', 'Linkedin Profil Linki'),
        ('social_youtube', '#', 'Youtube Kanal Linki'),
        ('social_whatsapp', '#', 'WhatsApp İletişim Hattı'),
        ('contact_email', 'info@imzagayrimenkul.com', 'Genel İletişim E-postası'),
        ('contact_phone', '+90 212 555 00 00', 'Genel İletişim Telefonu')
    ]

    for key, value, desc in settings:
        cursor.execute('INSERT OR IGNORE INTO site_settings (key, value, description) VALUES (?, ?, ?)', (key, value, desc))

    conn.commit()
    conn.close()
    print("Şema başarıyla güncellendi.")

if __name__ == "__main__":
    update_schema()
