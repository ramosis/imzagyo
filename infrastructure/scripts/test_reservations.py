import sys
import os
import sqlite3

# Add project root to path
# Adjusting to account for being in infrastructure/scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from modules.neighborhood.repository import ReservationRepository
from shared.database import get_db

def test_reservations():
    print("--- Testing Neighborhood Reservations ---")
    
    # 1. Clear existing test data if any
    with get_db() as conn:
        conn.execute("DELETE FROM neighborhood_reservations WHERE name = 'Antigravity Test'")
        conn.commit()
    
    test_data = {
        'facility_id': 'gym',
        'date': '2026-04-10',
        'time': '11:00',
        'name': 'Antigravity Test',
        'user_id': 1
    }
    
    # 2. Create reservation
    try:
        res_id = ReservationRepository.create(test_data)
        print(f"SUCCESS: Created reservation with ID {res_id}")
    except Exception as e:
        print(f"FAILED: create() error: {e}")
        return
    
    # 3. Check for conflict (double booking)
    try:
        ReservationRepository.create(test_data)
        print("FAILED: Double booking was allowed!")
    except ValueError as ve:
        print(f"SUCCESS: Collision detected as expected: {ve}")
    except Exception as e:
        print(f"FAILED: Unexpected error on conflict: {e}")
    
    # 4. Get by date range
    try:
        results = ReservationRepository.get_by_date_range('gym', '2026-04-01', '2026-04-30')
        found = any(r['name'] == 'Antigravity Test' for r in results)
        if found:
            print(f"SUCCESS: Found test reservation in range. Count: {len(results)}")
        else:
            print("FAILED: Test reservation not found in date range.")
    except Exception as e:
        print(f"FAILED: get_by_date_range() error: {e}")

if __name__ == "__main__":
    test_reservations()
