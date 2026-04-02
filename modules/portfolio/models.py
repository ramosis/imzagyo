from shared.extensions import db
import datetime as dt

class PortfolioListing(db.Model):
    __tablename__ = 'portfoyler'
    id = db.Column(db.String(50), primary_key=True)
    koleksiyon = db.Column(db.String(100), nullable=True)
    baslik1 = db.Column(db.String(255), nullable=True)
    baslik2 = db.Column(db.String(255), nullable=True)
    lokasyon = db.Column(db.String(255), nullable=True)
    refNo = db.Column(db.String(50), nullable=True)
    fiyat = db.Column(db.Float, nullable=True)
    oda = db.Column(db.String(20), nullable=True)
    alan = db.Column(db.String(20), nullable=True)
    kat = db.Column(db.String(20), nullable=True)
    ozellik_renk = db.Column(db.String(20), nullable=True)
    bg_renk = db.Column(db.String(20), nullable=True)
    btn_renk = db.Column(db.String(20), nullable=True)
    icon_renk = db.Column(db.String(20), nullable=True)
    resim_hero = db.Column(db.Text, nullable=True)
    resim_hikaye = db.Column(db.Text, nullable=True)
    hikaye = db.Column(db.Text, nullable=True)
    baslik1_en = db.Column(db.String(255), nullable=True)
    baslik1_ar = db.Column(db.String(255), nullable=True)
    baslik2_en = db.Column(db.String(255), nullable=True)
    baslik2_ar = db.Column(db.String(255), nullable=True)
    lokasyon_en = db.Column(db.String(255), nullable=True)
    lokasyon_ar = db.Column(db.String(255), nullable=True)
    hikaye_en = db.Column(db.Text, nullable=True)
    hikaye_ar = db.Column(db.Text, nullable=True)
    ozellikler = db.Column(db.Text, nullable=True) # JSON stored as text
    danisman_isim = db.Column(db.String(100), nullable=True)
    danisman_unvan = db.Column(db.String(100), nullable=True)
    danisman_resim = db.Column(db.Text, nullable=True)
    mulk_tipi = db.Column(db.String(50), default='Konut')
    alt_tip = db.Column(db.String(50), nullable=True)
    denetim_notlari = db.Column(db.Text, nullable=True)
    mahalle_id = db.Column(db.String(50), nullable=True)
    cephe = db.Column(db.String(50), nullable=True)
    gunes_bilgisi = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    is_sample = db.Column(db.Boolean, default=False)

    media = db.relationship('PortfolioMedia', backref='portfolio', lazy=True, cascade='all, delete-orphan')

class PortfolioMedia(db.Model):
    __tablename__ = 'portfoy_medya'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    category = db.Column(db.String(50), nullable=False) # iç, dış, drone, video, plan
    file_path = db.Column(db.Text, nullable=False)
    local_path = db.Column(db.Text, nullable=True)
    focal_x = db.Column(db.Float, nullable=True)
    focal_y = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class MLSListing(db.Model):
    __tablename__ = 'mls_listings'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    sharing_status = db.Column(db.String(20), default='private') # private, inner, outer
    commission_split = db.Column(db.Float, default=50.0)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class MLSDemand(db.Model):
    __tablename__ = 'mls_demands'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False) # Talep sahibi danışman/ofis
    category = db.Column(db.String(50), nullable=True)
    region = db.Column(db.String(100), nullable=True)
    budget_max = db.Column(db.Float, nullable=True)
    features_json = db.Column(db.Text, nullable=True) # JSON stored as text
    status = db.Column(db.String(20), default='open') # open, matched, closed
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class MLSTrustScore(db.Model):
    __tablename__ = 'mls_trust_scores'
    office_id = db.Column(db.String(50), primary_key=True)
    score = db.Column(db.Float, default=5.0)
    review_count = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=dt.datetime.utcnow, onupdate=dt.datetime.utcnow)

class Ekip(db.Model):
    __tablename__ = 'ekip'
    id = db.Column(db.String(50), primary_key=True)
    isim = db.Column(db.String(100), nullable=True)
    unvan = db.Column(db.String(100), nullable=True)
    detaylar = db.Column(db.Text, nullable=True) # JSON stored as text
    uzmanlikAlanlari = db.Column(db.Text, nullable=True) # JSON stored as text
    telefon = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    resim = db.Column(db.Text, nullable=True)
    sosyal_linkedin = db.Column(db.String(255), nullable=True)
    sosyal_instagram = db.Column(db.String(255), nullable=True)
    sosyal_twitter = db.Column(db.String(255), nullable=True)
    tip = db.Column(db.String(20), nullable=True) # yonetici, danisman

class PropertyInspection(db.Model):
    __tablename__ = 'property_inspections'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    portfolio_id = db.Column(db.String(50), db.ForeignKey('portfoyler.id', ondelete='CASCADE'), nullable=False)
    staff_id = db.Column(db.String(50), nullable=True)
    inspection_date = db.Column(db.DateTime, default=dt.datetime.utcnow)
    category = db.Column(db.String(50), nullable=True) # Konut, Ticari, Arazi
    data_json = db.Column(db.Text, nullable=True) # JSON stored as text
    score_summary = db.Column(db.String(255), nullable=True)
    overall_score = db.Column(db.Float, nullable=True)
    notes = db.Column(db.Text, nullable=True)

class ListingShadow(db.Model):
    __tablename__ = 'listings_shadow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    price = db.Column(db.String(100), nullable=True)
    price_numeric = db.Column(db.Float, nullable=True)
    estimated_rent = db.Column(db.Float, nullable=True)
    roi_score = db.Column(db.Float, nullable=True)
    amortization_years = db.Column(db.Float, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    district = db.Column(db.String(100), nullable=True)
    neighborhood = db.Column(db.String(100), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    url = db.Column(db.Text, unique=True, nullable=True)
    source = db.Column(db.String(50), nullable=True) # sahibinden, hepsiemlak
    listing_type = db.Column(db.String(50), nullable=True) # Satılık, Kiralık
    owner_name = db.Column(db.String(100), nullable=True)
    owner_phone = db.Column(db.String(50), nullable=True)
    listing_date = db.Column(db.String(50), nullable=True)
    data_json = db.Column(db.Text, nullable=True)
    last_seen_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    hero_image_url = db.Column(db.Text, nullable=True)
    theme_color = db.Column(db.String(20), default='#000000')
    features = db.Column(db.Text, nullable=True) # JSON stored as text
    price_range = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)

class ProjectLead(db.Model):
    __tablename__ = 'project_leads'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='new')
    pipeline_stage_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=dt.datetime.utcnow)
