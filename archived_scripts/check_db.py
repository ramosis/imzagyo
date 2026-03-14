import sqlite3
import os

db_path = 'imzagayrimenkul.db'
if not os.path.exists(db_path):
    print(f"DB not found at {db_path}")
    exit(1)

conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Examine schema of appointments
cur.execute("PRAGMA table_info(appointments)")
print("Appointments table columns:")
for row in cur.fetchall():
    print(row)

# Examine schema of contracts
cur.execute("PRAGMA table_info(contracts)")
print("\nContracts table columns:")
for row in cur.fetchall():
    print(row)

conn.close()
