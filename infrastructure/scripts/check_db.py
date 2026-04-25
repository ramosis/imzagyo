import sqlite3
import os

db_path = 'g:/Antigravity Projects/Imza_Gayrimenkul/Imza_Gayrimenkul.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    print("Tables:", tables)
    for table in tables:
        if table[0] in ['projects', 'ekip', 'portfoyler', 'mahalleler']:
            cur.execute(f"PRAGMA table_info({table[0]})")
            print(f"Schema for {table[0]}:", cur.fetchall())
    conn.close()
else:
    print("DB not found at", db_path)
