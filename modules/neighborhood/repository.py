from typing import List, Dict, Any, Optional
from shared.extensions import db
from .models import NeighborhoodReservation, NeighborhoodFacility
from sqlalchemy import and_

class ReservationRepository:
    """Handles database operations for Neighborhood Reservations using SQLAlchemy ORM."""
    
    @staticmethod
    def get_by_date_range(facility_id: str, start_date: str, end_date: str) -> List[NeighborhoodReservation]:
        """Returns confirmed reservations for a facility within a date range."""
        return NeighborhoodReservation.query.filter(
            and_(
                NeighborhoodReservation.facility_id == facility_id,
                NeighborhoodReservation.date >= start_date,
                NeighborhoodReservation.date <= end_date,
                NeighborhoodReservation.status != 'cancelled'
            )
        ).all()

    @staticmethod
    def create(data: Dict[str, Any]) -> NeighborhoodReservation:
        """Creates a new reservation with smart capacity check."""
        facility_id = data.get('facility_id')
        date = data.get('date')
        time_slot = data.get('time_slot') or data.get('time')
        
        # 1. Fetch facility for capacity info
        facility = db.session.get(NeighborhoodFacility, facility_id)
        if not facility:
            raise ValueError(f"Facility '{facility_id}' not found.")
            
        max_cap = facility.max_capacity or 1
        
        # 2. Check current occupancy for this slot
        occupancy = NeighborhoodReservation.query.filter_by(
            facility_id=facility_id,
            date=date,
            time_slot=time_slot,
            status='confirmed'
        ).count()
        
        if occupancy >= max_cap:
            raise ValueError(f"Bu saat dilimi için kapasite ({max_cap}) dolmuştur.")
            
        # 3. Create reservation
        reservation = NeighborhoodReservation(
            facility_id=facility_id,
            date=date,
            time_slot=time_slot,
            name=data.get('name'),
            user_id=data.get('user_id'),
            status='confirmed'
        )
        
        db.session.add(reservation)
        db.session.commit()
        return reservation

    @staticmethod
    def cancel(reservation_id: int) -> bool:
        """Cancels an existing reservation."""
        res = db.session.get(NeighborhoodReservation, reservation_id)
        if res:
            res.status = 'cancelled'
            db.session.commit()
            return True
        return False
