import sqlite3
import os

# Get database path relative to project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "data", "imza_database.db")

def apply_index():
    if not os.path.exists(DB_NAME):
        print(f"Error: Database not found at {DB_NAME}")
        return
        
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("Applying performance indexes...")
    try:
        # Index for CRM Lead Scoring (Most likely bottleneck)
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_interactions_session ON user_interactions(session_id);')
        
        # Index for Portal Reservations
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_reservations_date ON reservations(date);')
        
        # Index for Portfolio search
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_portfolios_owner ON portfoyler(owner_id);')
        
        conn.commit()
        print("Success: Indexes applied successfully.")
    except sqlite3.Error as e:
        print(f"Error applying indexes: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    apply_index()
