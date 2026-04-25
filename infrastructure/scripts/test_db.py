import sqlite3
import json

conn = sqlite3.connect('imza_database.db')
conn.row_factory = sqlite3.Row
ekip = conn.execute('SELECT * FROM ekip').fetchall()

for e in ekip:
    d = dict(e)
    print(f"ID: {d['id']}")
    print(f"Detaylar Is String: {isinstance(d['detaylar'], str)}")
    print(f"Detaylar Value: {d['detaylar']}")
    print("---")

conn.close()
