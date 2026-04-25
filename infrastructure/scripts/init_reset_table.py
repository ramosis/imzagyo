import sqlite3

def check_reset_table():
    conn = sqlite3.connect('data/imza.db')
    cursor = conn.cursor()
    
    # password_resets tablosunu kontrol et
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password_resets'")
    exists = cursor.fetchone()
    
    if not exists:
        print("password_resets tablosu oluşturuluyor...")
        cursor.execute('''
            CREATE TABLE password_resets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                token TEXT NOT NULL UNIQUE,
                expiry DATETIME NOT NULL,
                used INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        conn.commit()
    else:
        print("password_resets tablosu zaten mevcut.")
        
    conn.close()

if __name__ == '__main__':
    check_reset_table()
