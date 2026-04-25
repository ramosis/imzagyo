import sqlite3
import os

DB_PATH = "g:\\Antigravity Projects\\Imza_Gayrimenkul\\data\\imza_database.db"
SQL_PATH = "g:\\Antigravity Projects\\Imza_Gayrimenkul\\scripts\\migration_3mode.sql"

def run_migration():
    if not os.path.exists(DB_PATH):
        print(f"Error: Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SQL_PATH, 'r', encoding='utf-8') as f:
        sql_commands = f.read().split(';')

    for command in sql_commands:
        if command.strip():
            try:
                cursor.execute(command)
                print(f"Executed: {command[:50]}...")
            except sqlite3.OperationalError as e:
                print(f"Skipped (likely already exists): {e}")

    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    run_migration()
