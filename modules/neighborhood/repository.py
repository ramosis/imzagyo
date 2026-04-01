from typing import List, Dict, Any, Optional
from shared.database import get_db
from datetime import datetime

class ReservationRepository:
    """Handles low-level SQL operations for Neighborhood Reservations (Facilities, Gym, Pool, etc)."""
    
    @staticmethod
    def get_by_date_range(facility_id: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
        with get_db() as conn:
            query = '''
                SELECT id, facility_id, date as reservation_date, time_slot, name, status 
                FROM neighborhood_reservations 
                WHERE facility_id = ? AND date BETWEEN ? AND ? AND status != 'cancelled'
            '''
            rows = conn.execute(query, (facility_id, start_date, end_date)).fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            # Prevent double booking using a quick check
            check = conn.execute(
                'SELECT id FROM neighborhood_reservations WHERE facility_id=? AND date=? AND time_slot=? AND status != "cancelled"',
                (data.get('facility_id'), data.get('date'), data.get('time'))
            ).fetchone()
            
            if check:
                raise ValueError("This time slot is already booked.")
                
            cursor = conn.execute('''
                INSERT INTO neighborhood_reservations (facility_id, date, time_slot, name, user_id, status) 
                VALUES (?, ?, ?, ?, ?, 'confirmed')
            ''', (
                data.get('facility_id'),
                data.get('date'),
                data.get('time'),
                data.get('name'),
                data.get('user_id')
            ))
            conn.commit()
            return cursor.lastrowid
