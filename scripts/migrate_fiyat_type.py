import sqlite3
import os

DB_NAME = "data/imza_database.db"

def migrate():
    if not os.path.exists(DB_NAME):
        print("Database not found.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    print("Starting corrected migration: portfoyler.fiyat TEXT -> REAL")

    try:
        # 1. Create a temporary table with the new schema (including all Phase 8 columns)
        cursor.execute("DROP TABLE IF EXISTS portfoyler_new")
        cursor.execute('''
            CREATE TABLE portfoyler_new (
                id TEXT PRIMARY KEY,
                koleksiyon TEXT,
                baslik1 TEXT,
                baslik2 TEXT,
                lokasyon TEXT,
                refNo TEXT,
                fiyat REAL,
                oda TEXT,
                alan TEXT,
                kat TEXT,
                ozellik_renk TEXT,
                bg_renk TEXT,
                btn_renk TEXT,
                icon_renk TEXT,
                resim_hero TEXT,
                resim_hikaye TEXT,
                hikaye TEXT,
                ozellikler TEXT,
                danisman_isim TEXT,
                danisman_unvan TEXT,
                danisman_resim TEXT,
                mulk_tipi TEXT DEFAULT 'Konut',
                alt_tip TEXT,
                denetim_notlari TEXT,
                mahalle_id TEXT, -- New Phase 8
                cephe TEXT,
                gunes_bilgisi TEXT,
                owner_id INTEGER REFERENCES users(id) -- New Phase 8
            )
        ''')

        # 2. Copy data from old to new (matching ONLY current 26 columns)
        # Current columns in source: id, koleksiyon, baslik1, baslik2, lokasyon, refNo, fiyat, oda, alan, kat,
        # ozellik_renk, bg_renk, btn_renk, icon_renk, resim_hero, resim_hikaye, hikaye, ozellikler,
        # danisman_isim, danisman_unvan, danisman_resim, mulk_tipi, alt_tip, denetim_notlari, cephe, gunes_bilgisi
        
        cursor.execute('''
            INSERT INTO portfoyler_new 
            (id, koleksiyon, baslik1, baslik2, lokasyon, refNo, fiyat, oda, alan, kat,
             ozellik_renk, bg_renk, btn_renk, icon_renk, resim_hero, resim_hikaye, hikaye, ozellikler,
             danisman_isim, danisman_unvan, danisman_resim, mulk_tipi, alt_tip, denetim_notlari,
             cephe, gunes_bilgisi)
            SELECT id, koleksiyon, baslik1, baslik2, lokasyon, refNo, 
                   CAST(REPLACE(REPLACE(fiyat, '.', ''), ',', '.') AS REAL),
                   oda, alan, kat, ozellik_renk, bg_renk, btn_renk, icon_renk, 
                   resim_hero, resim_hikaye, hikaye, ozellikler, danisman_isim, 
                   danisman_unvan, danisman_resim, mulk_tipi, alt_tip, 
                   denetim_notlari, cephe, gunes_bilgisi
            FROM portfoyler
        ''')

        # 3. Drop old table and rename new
        cursor.execute("DROP TABLE portfoyler")
        cursor.execute("ALTER TABLE portfoyler_new RENAME TO portfoyler")

        conn.commit()
        print("Migration successful: portfoyler.fiyat is now REAL and Phase 8 columns added.")

    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
