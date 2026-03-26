import os
import sys

# Move to the project root directory
os.chdir(r'g:\Antigravity Projects\İmza Gayrimenkul')
sys.path.append(os.getcwd())

from app import app
from database import get_db_connection

def test_pusula():
    with app.app_context():
        # Insert a dummy lead for testing
        conn = get_db_connection()
        conn.execute("INSERT OR IGNORE INTO leads (name, email, status) VALUES ('Test Müşteri', 'test@test.com', 'Ayricalikli')")
        conn.commit()
        
        lead_id = conn.execute("SELECT id FROM leads ORDER BY id DESC LIMIT 1").fetchone()['id']
        conn.close()

        print(f"--- Creating Magic Link for Lead ID: {lead_id} ---")
        from api.compass import generate_magic_link
        token = generate_magic_link(lead_id)
        print(f"Generated Token: {token[:20]}...")

        print("\n--- Testing API Endpoint ---")
        client = app.test_client()
        res = client.get('/api/compass/data', headers={'Authorization': f'Bearer {token}'})
        
        print(f"Status Code: {res.status_code}")
        print("Response JSON:")
        import json
        print(json.dumps(res.get_json(), indent=2, ensure_ascii=False))

if __name__ == '__main__':
    test_pusula()
