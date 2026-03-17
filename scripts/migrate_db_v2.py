import sqlite3

def run_migration():
    conn = sqlite3.connect('data/imza.db')
    cursor = conn.cursor()
    
    # Çeviri kolonlarını ekle
    columns_to_add = [
        ('baslik1_en', 'TEXT'),
        ('baslik1_ar', 'TEXT'),
        ('baslik2_en', 'TEXT'),
        ('baslik2_ar', 'TEXT'),
        ('lokasyon_en', 'TEXT'),
        ('lokasyon_ar', 'TEXT'),
        ('hikaye_en', 'TEXT'),
        ('hikaye_ar', 'TEXT')
    ]
    
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f"ALTER TABLE portfoyler ADD COLUMN {col_name} {col_type}")
            print(f"Kolon eklendi: {col_name}")
        except sqlite3.OperationalError:
            print(f"Kolon zaten mevcut: {col_name}")
            
    conn.commit()
    conn.close()

if __name__ == '__main__':
    run_migration()
