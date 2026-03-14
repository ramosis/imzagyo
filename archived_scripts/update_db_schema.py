import sqlite3

def update_db():
    conn = sqlite3.connect('imza_database.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN seller_id INTEGER;")
    except Exception as e: print(e)
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN buyer_id INTEGER;")
    except Exception as e: print(e)
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN contract_type TEXT;")
    except Exception as e: print(e)
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN special_conditions TEXT;")
    except Exception as e: print(e)
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN status TEXT DEFAULT 'draft';")
    except Exception as e: print(e)
    try:
        cursor.execute("ALTER TABLE contracts ADD COLUMN created_at TIMESTAMP;")
    except Exception as e: print(e)
    try:
        cursor.execute("UPDATE contracts SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;")
    except Exception as e: print(e)
    conn.commit()
    print("Columns added successfully.")
    conn.close()

if __name__ == '__main__':
    update_db()
