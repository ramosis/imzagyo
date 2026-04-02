from shared.extensions import db
import datetime as dt

class NeighborhoodFacility(db.Model):
    __tablename__ = 'neighborhood_facilities'
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    icon = db.Column(db.String(50), nullable=True)
    receipt_url = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    max_capacity = db.Column(db.Integer, default=1) # Phase 27: Smart capacity control

class NeighborhoodReservation(db.Model):
    __tablename__ = 'neighborhood_reservations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    facility_id = db.Column(db.String(50), db.ForeignKey('neighborhood_facilities.id', ondelete='CASCADE'), nullable=False)
    date = db.Column(db.String(20), nullable=False) # YYYY-MM-DD
    time_slot = db.Column(db.String(20), nullable=False) # HH:MM
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status = db.Column(db.String(20), default='confirmed') # confirmed, cancelled
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ApartmentPoll(db.Model):
    __tablename__ = 'apartment_polls'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mahalle_id = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    options = db.Column(db.Text, nullable=True) # JSON list
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class PollVote(db.Model):
    __tablename__ = 'poll_votes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('apartment_polls.id', ondelete='CASCADE'), nullable=False)
    user_name = db.Column(db.String(100), nullable=True)
    selected_option = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ShuttleSchedule(db.Model):
    __tablename__ = 'shuttle_schedule'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    route_name = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.String(10), nullable=False) # HH:MM
    estimated_arrival = db.Column(db.String(10), nullable=True)

class StaffLocation(db.Model):
    __tablename__ = 'staff_locations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    location_type = db.Column(db.String(20), nullable=True) # checkin, periodic, assigned
    updated_at = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

class Business(db.Model):
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False) # Tesisatçi, Restoran, Market...
    description = db.Column(db.Text, nullable=True)
    phone = db.Column(db.String(50), nullable=True)
    address = db.Column(db.Text, nullable=True)
    logo_url = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Float, default=0.0)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class NeighborhoodPost(db.Model):
    __tablename__ = 'neighborhood_posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # duyuru, ulasim, paylasim, yardim
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class NeighborhoodDemand(db.Model):
    __tablename__ = 'neighborhood_demands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(50), nullable=False) # Gayrimenkul, Hizmet, Organizasyon, Diger
    content = db.Column(db.Text, nullable=False)
    user_name = db.Column(db.String(100), nullable=True)
    user_phone = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='open') # open, in_progress, resolved
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
