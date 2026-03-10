"""
Database Patch Script for AI Features

This script adds the 'market_stats' table to the existing 'imza_database.db'
to store time-series data from external sources like TCMB.
"""
import sqlite3
import os

DB_NAME = "imza_database.db"

def apply_patch():
    """
    Adds the market_stats table to the database if it doesn't exist.
    """
    if not os.path.exists(DB_NAME):
        print(f"Hata: '{DB_NAME}' veritabanı bulunamadı. Lütfen önce ana veritabanını oluşturun.")
        return

    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        # Check if the table already exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='market_stats'")
        if cursor.fetchone():
            print("'market_stats' tablosu zaten mevcut. Herhangi bir değişiklik yapılmadı.")
            return

        print("'market_stats' tablosu oluşturuluyor...")
        # Create the new table for market statistics
        cursor.execute('''
            CREATE TABLE market_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                region_name TEXT NOT NULL,
                series_code TEXT NOT NULL,
                series_name TEXT,
                value REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(date, region_name, series_code)
            )
        ''')
        
        conn.commit()
        print("'market_stats' tablosu başarıyla veritabanına eklendi.")

    except sqlite3.Error as e:
        print(f"Veritabanı hatası: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    apply_patch()
