""" 
Database Management Module
Handles SQLite database initialization, connection management, and sample data population.
"""
import sqlite3
import json
import os
import hashlib
import bcrypt
from contextlib import contextmanager

DB_NAME = "data/imza_database.db"

def get_db_connection():
    """Returns a sqlite3 connection object with row_factory set to Row."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

@contextmanager
def get_db():
    """Context manager for database connections (Section 5.3)."""
    conn = get_db_connection()
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initializes the database, creates tables, and inserts a default admin user."""
    # Eski veritabanını silmeyi durduruyoruz (Veri kaybını önlemek ve Docker hatalarını gidermek için)
    # Eğer Dosya yerine yanlışlıkla Klasör oluşmuşsa uyarı ver
    if os.path.exists(DB_NAME) and os.path.isdir(DB_NAME):
        print(f"HATA: {DB_NAME} bir klasör olarak görünüyor! Lütfen sunucudaki bu klasörü silin.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- Temel Tablolar (Bağımlılığı Olmayanlar) ---

    # Kullanıcılar
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT UNIQUE,
            is_admin BOOLEAN DEFAULT 0,
            role TEXT NOT NULL CHECK(role IN ("admin","super_admin","broker","danisman","vip","kiraci","muteahhit","standart","employee","owner","tenant","partner"))
        )
    ''')
    
    # Social Login alanlarını ekle (Mevcut veritabanını bozmamak için try-except kullanıyoruz)
    # Upgrade users table
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN email TEXT UNIQUE')
    except sqlite3.OperationalError: pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0')
    except sqlite3.OperationalError: pass
    try:
        cursor.execute('ALTER TABLE users ADD COLUMN social_provider TEXT')
        cursor.execute('ALTER TABLE users ADD COLUMN social_id TEXT')
        cursor.execute('ALTER TABLE users ADD COLUMN profile_pic TEXT')
    except sqlite3.OperationalError:
        pass # Kolonlar zaten eklenmişse hatayı yoksay
    # Portföyler (Mülkler)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfoyler (
            id TEXT PRIMARY KEY,
            koleksiyon TEXT,
            baslik1 TEXT,
            baslik2 TEXT,
            lokasyon TEXT,
            refNo TEXT,
            fiyat REAL,
            oda TEXT,
            alan TEXT,
            kat TEXT,
            ozellik_renk TEXT,
            bg_renk TEXT,
            btn_renk TEXT,
            icon_renk TEXT,
            resim_hero TEXT,
            resim_hikaye TEXT,
            hikaye TEXT,
            ozellikler TEXT, -- JSON formatında liste
            danisman_isim TEXT,
            danisman_unvan TEXT,
            danisman_resim TEXT,
            mulk_tipi TEXT DEFAULT 'Konut',
            alt_tip TEXT, -- Daire, Villa, Ofis, Arsa vb.
            denetim_notlari TEXT,
            mahalle_id TEXT, -- İmza Mahalle eşleşmesi için
            cephe TEXT, -- Kuzey, Güney, Doğu, Batı, vb.
            gunes_bilgisi TEXT, -- Metinsel güneş analizi
            owner_id INTEGER REFERENCES users(id)
        )
    ''')
    
    # Yeni sütunları mevcut tabloya ekleme (Upgrade logic)
    try:
        cursor.execute('ALTER TABLE portfoyler ADD COLUMN cephe TEXT')
        cursor.execute('ALTER TABLE portfoyler ADD COLUMN gunes_bilgisi TEXT')
        cursor.execute('ALTER TABLE portfoyler ADD COLUMN owner_id INTEGER REFERENCES users(id)')
    except sqlite3.OperationalError:
        pass # Kolonlar zaten eklenmişse hatayı yoksay

    # Pipeline Aşamaları
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pipeline_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            order_index INTEGER DEFAULT 0,
            color TEXT, -- Frontend'de sütun başlığı rengi için
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Sözleşme Şablon Tipleri
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')

    # Sözleşme Maddeleri (Clauses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract_clauses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_id INTEGER NOT NULL,
            clause_text TEXT NOT NULL,
            is_mandatory BOOLEAN DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            FOREIGN KEY(template_id) REFERENCES contract_templates(id)
        )
    ''')

    # Taraflar (Müşteriler, Satıcılar vb.)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tc_no TEXT UNIQUE,
            vkn TEXT UNIQUE,
            party_type TEXT NOT NULL CHECK(party_type IN ('individual', 'corporate')),
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Saha Personeli Konum Takibi (Staff Tracking)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS staff_locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_type TEXT, -- 'checkin', 'periodic', 'assigned'
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Şifre Sıfırlama (HATA-002)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL,
            expiry TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # --- Neighborhood & Facilities (Mahalle Özellikleri) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neighborhood_facilities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            icon TEXT, -- Eksik olan icon kolonu eklendi
            receipt_url TEXT,
            description TEXT
        )
    ''')

    # Eğer tablo daha önce yaratıldıysa icon kolonunu eklemeyi dene
    try:
        cursor.execute('ALTER TABLE neighborhood_facilities ADD COLUMN icon TEXT')
    except sqlite3.OperationalError:
        pass

    # --- PLAN 3.2: COMMUNITY & POLLS ---
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS apartment_polls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mahalle_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        options TEXT, -- JSON list: ["Seçenek 1", "Seçenek 2"]
        expires_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS poll_votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        poll_id INTEGER,
        user_name TEXT,
        selected_option TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (poll_id) REFERENCES apartment_polls(id)
    )''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS shuttle_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            estimated_arrival TEXT
        )
    ''')

    # Örnek Tesisler
    cursor.execute('INSERT OR IGNORE INTO neighborhood_facilities (id, name, category, icon, description) VALUES (?, ?, ?, ?, ?)',
                   ('gym', 'Fitness Center', 'Sport', 'fa-dumbbell', 'Modern ekipmanlarla donatılmış spor salonu.'))
    cursor.execute('INSERT OR IGNORE INTO neighborhood_facilities (id, name, category, icon, description) VALUES (?, ?, ?, ?, ?)',
                   ('pool', 'Açık Havuz', 'Sport', 'fa-person-swimming', 'Yaz aylarında kullanıma açık vadi manzaralı havuz.'))
    cursor.execute('INSERT OR IGNORE INTO neighborhood_facilities (id, name, category, icon, description) VALUES (?, ?, ?, ?, ?)',
                   ('cinema', 'Cep Sineması', 'Entertainment', 'fa-film', 'Ailenizle film keyfi yapabileceğiniz özel salon.'))

    # Örnek Shuttle
    cursor.execute('INSERT OR IGNORE INTO shuttle_schedule (route_name, departure_time, estimated_arrival) VALUES (?, ?, ?)',
                   ('Maslak Metro - Site', '08:30', '08:45'))
    cursor.execute('INSERT OR IGNORE INTO shuttle_schedule (route_name, departure_time, estimated_arrival) VALUES (?, ?, ?)',
                   ('Site - Maslak Metro', '09:00', '09:15'))

    # (portfoyler table moved to top)

    # Media table for portfolio images/videos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfoy_medya (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id TEXT NOT NULL,
            category TEXT NOT NULL, -- iç, dış, drone, video, plan
            file_path TEXT NOT NULL,
            local_path TEXT, -- Server-side relative path
            focal_x REAL, -- percentage (0-100)
            focal_y REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(portfolio_id) REFERENCES portfoyler(id)
        )
    ''')

    # Ekip Tablosu (Tam olarak ekip-data.js'deki alanlarla eşleşecek)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ekip (
            id TEXT PRIMARY KEY,
            isim TEXT,
            unvan TEXT,
            detaylar TEXT,      -- Liste, JSON
            uzmanlikAlanlari TEXT, -- Liste, JSON
            telefon TEXT,
            email TEXT,
            resim TEXT,
            sosyal_linkedin TEXT,
            sosyal_instagram TEXT,
            sosyal_twitter TEXT,
            tip TEXT            -- "yonetici" veya "danisman"
        )
    ''')

    # New tables for expanded functionality
    # (users table moved to top)
    # --- Plan 12: Dijital Konut Denetim & Ekspertiz Formu ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS property_inspections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id TEXT NOT NULL,
            staff_id TEXT,
            inspection_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            category TEXT, -- Konut, Ticari, Arazi
            data_json TEXT, -- Tüm kontrol listesi verileri (JSON)
            score_summary TEXT, -- Puan özeti (Yeşil/Sarı/Kırmızı sayıları)
            overall_score REAL,
            notes TEXT,
            FOREIGN KEY(portfolio_id) REFERENCES portfoyler(id)
        )
    ''')

    # --- Plan 13: MLS (Multiple Listing Service) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mls_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            portfolio_id TEXT NOT NULL,
            sharing_status TEXT DEFAULT 'private', -- private, inner, outer
            commission_split REAL DEFAULT 50.0, -- Yüzde (%50 paylaşımlı)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(portfolio_id) REFERENCES portfoyler(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mls_demands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL, -- Talep sahibi danışman/ofis
            category TEXT, -- Konut, Ticari vb.
            region TEXT,
            budget_max REAL,
            features_json TEXT,
            status TEXT DEFAULT 'open', -- open, matched, closed
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mls_trust_scores (
            office_id TEXT PRIMARY KEY,
            score REAL DEFAULT 5.0,
            review_count INTEGER DEFAULT 0,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            seller_id INTEGER,
            buyer_id INTEGER,
            contract_type TEXT,
            special_conditions TEXT,
            status TEXT DEFAULT 'draft',
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(seller_id) REFERENCES parties(id),
            FOREIGN KEY(buyer_id) REFERENCES parties(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taxes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            tax_type TEXT, -- Emlak Vergisi, Aidat, Sigorta vb.
            amount REAL,
            due_date TEXT,
            status TEXT DEFAULT 'Ödenmedi', -- Ödendi, Ödenmedi, Gecikmiş
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS maintenance_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            user_id INTEGER, -- Talep eden kullanıcı
            title TEXT, -- Başlık
            description TEXT,
            priority TEXT DEFAULT 'Normal', -- Düşük, Normal, Yüksek, Acil
            request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scheduled_date TEXT,
            status TEXT DEFAULT 'Açık', -- Açık, İşlemde, Çözüldü, İptal
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS property_units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            unit_number TEXT NOT NULL,
            floor TEXT,
            unit_type TEXT DEFAULT 'Konut',
            area_sqm REAL,
            status TEXT DEFAULT 'Boş', -- Boş, Dolu, Tadilatta
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_unit_id INTEGER NOT NULL,
            tenant_id INTEGER NOT NULL,
            start_date TEXT,
            end_date TEXT,
            rent_amount REAL,
            currency TEXT DEFAULT 'TRY',
            payment_day INTEGER, 
            deposit_amount REAL,
            status TEXT DEFAULT 'Aktif', -- Aktif, Sonlandı
            contract_file TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_unit_id) REFERENCES property_units(id),
            FOREIGN KEY(tenant_id) REFERENCES users(id)
        )
    ''')
    
    # Yeni Eklenen: Aidat, Kira ve Ekstra Ödemeler tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dues_payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lease_id INTEGER,
            property_unit_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL, -- Ödemeyi yapan kişi
            payment_type TEXT DEFAULT 'AIDAT', -- AIDAT, DEMIRBAS, KIRA, EKSTRA
            amount REAL NOT NULL,
            status TEXT DEFAULT 'Ödenmedi', -- Ödenmedi, Ödendi, Gecikmiş
            due_date TEXT NOT NULL,
            paid_date TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(lease_id) REFERENCES leases(id),
            FOREIGN KEY(property_unit_id) REFERENCES property_units(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Yeni Eklenen: Apartman ve Site Giderleri (Kasa) Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS apartment_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL, -- Hangi apartman/bina (portföy)
            expense_type TEXT, -- Temizlik, Asansör Bakımı, Elektrik, Su
            amount REAL NOT NULL,
            expense_date TEXT NOT NULL,
            invoice_file TEXT, -- Fatura/Dekont Upload URL
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            property_id TEXT,
            client_name TEXT,
            client_phone TEXT,
            datetime TEXT,
            purpose TEXT DEFAULT 'gosterim',
            notes TEXT,
            assigned_user_id INTEGER,
            pipeline_stage_id INTEGER, -- Added missing column
            original_datetime TEXT,
            reschedule_count INTEGER DEFAULT 0,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(assigned_user_id) REFERENCES users(id),
            FOREIGN KEY(pipeline_stage_id) REFERENCES pipeline_stages(id)
        )
    ''')

    # Hero (Slider) CMS Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hero_slides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resim_url TEXT NOT NULL,
            alt_baslik TEXT,
            baslik_satir1 TEXT,
            baslik_satir2 TEXT,
            buton1_metin TEXT,
            buton2_metin TEXT,
            buton2_link TEXT,
            sira INTEGER DEFAULT 0
        )
    ''')

    # (contract_templates and clauses moved/consolidated)


    # (parties table moved to top)

    # Hazırlanan / Kaydedilen Sözleşmeler
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prepared_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            template_id INTEGER NOT NULL,
            user_id INTEGER, -- Sözleşmeyi hazırlayan veya muhatap
            content_json TEXT, -- Seçilen maddeler ve doldurulan verilerin JSON hali
            seller_parties TEXT, -- Satıcı tarafların JSON listesi
            buyer_parties TEXT, -- Alıcı tarafların JSON listesi
            status TEXT DEFAULT 'draft', -- draft, signed, cancelled, finalized
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(template_id) REFERENCES contract_templates(id)
        )
    ''')

    # --- CRM ve Otomasyon Tabloları (YENİ) ---

    # Müşteri Adayları (Leads)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            source TEXT, -- 'website', 'sahibinden', 'referans', 'instagram'
            interest_property_id TEXT, -- İlgilendiği portföy ID (Opsiyonel)
            campaign_id TEXT, -- Aktif kampanya ID
            assigned_user_id INTEGER, -- Atanan Danışman
            status TEXT DEFAULT 'new',
            pipeline_stage_id INTEGER, -- new, contacted, qualified, lost, converted
            ai_score INTEGER DEFAULT 0, -- Yapay zeka öncelik puanı (0-100)
            segment TEXT, -- 'yatirimci', 'butce_odakli', 'yasam_tarzi', 'acil', 'buyuk_balik'
            score_x INTEGER DEFAULT 50, -- Alım Gücü (0-100)
            score_y INTEGER DEFAULT 50, -- Aciliyet/Sıcaklık (0-100)
            score_z INTEGER DEFAULT 50, -- Portföy Uyumu (0-100)
            last_contacted_at TIMESTAMP, -- Son görüşme tarihi (Sıralama için kritik)
            tags TEXT, -- JSON formatında etiketler: ["kopek_var", "kredi_istiyor", "roi_hesapladi"]
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(interest_property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(assigned_user_id) REFERENCES users(id),
            FOREIGN KEY(pipeline_stage_id) REFERENCES pipeline_stages(id)
        )
    ''')

    # Pipeline Geçiş Tarihçesi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pipeline_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            old_stage_id INTEGER,
            new_stage_id INTEGER NOT NULL,
            user_id INTEGER,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(lead_id) REFERENCES leads(id),
            FOREIGN KEY(old_stage_id) REFERENCES pipeline_stages(id),
            FOREIGN KEY(new_stage_id) REFERENCES pipeline_stages(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Varsayılan Aşamaları Ekle (Eğer tablo boşsa)
    cursor.execute('SELECT COUNT(*) FROM pipeline_stages')
    if cursor.fetchone()[0] == 0:
        default_stages = [
            ('Yeni Aday', 1, '#60a5fa'),      # Mavi
            ('İletişim Kuruldu', 2, '#fbbf24'), # Kehribar
            ('Sunum / Randevu', 3, '#a78bfa'),   # Mor
            ('Teklif Verildi', 4, '#fb923c'),    # Turuncu
            ('Sözleşme / Satış', 5, '#34d399'),  # Yeşil
            ('Kaybedildi', 6, '#f87171')        # Kırmızı
        ]
        cursor.executemany('INSERT INTO pipeline_stages (name, order_index, color) VALUES (?, ?, ?)', default_stages)
    
    # --- TODO: SATIŞ HUNİSİ VE MOBİL UYGULAMA İÇİN VERİTABANI PLANLAMASI ---
    # 1. Yeni Tablo: pipeline_stages
    #    - Sütunlar: id, name (Yeni, İletişim, Randevu, Teklif, Satış, Olumsuz), order_index
    #    - Amaç: Statik durumlar yerine yönetilebilir aşamalar oluşturmak.
    #
    # 2. Yeni Tablo: lead_activities
    #    - Sütunlar: id, lead_id, user_id, activity_type (call, note, meeting, checkin), 
    #                details, location_lat, location_long, created_at
    #    - Amaç: Müşteri tarihçesi ve saha ekibi takibi (GPS Check-in).
    
    # 3. Yeni Tablo: lead_interactions (Müşteri Dijital Ayak İzi)
    #    - Amaç: Müşterinin hesaplama araçlarıyla yaptığı işlemleri kaydetmek.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lead_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER, -- Eğer lead oluşmuşsa
            session_id TEXT, -- Henüz kayıt olmadıysa tarayıcı oturumu
            tool_name TEXT, -- 'roi_calculator', 'purchasing_power', 'lifestyle_matcher'
            data_json TEXT, -- Hesapladığı veriler (Örn: {"butce": 5000000, "kredi": true})
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Yeni Tablo: message_templates (WhatsApp/SMS Şablonları)
    #    - Amaç: Mesaj metinlerini koddan çıkarıp yönetilebilir hale getirmek.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS message_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            segment TEXT NOT NULL, -- 'yatirimci', 'butce_odakli', 'yasam_tarzi', 'buyuk_balik', 'acil', 'default'
            context_type TEXT NOT NULL, -- 'property' (Portföy ile), 'general' (Genel)
            template_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 5. Yeni Tablo: contacts (Premium Telefon Rehberi)
    #    - Amaç: Müşterilerin kişisel ve demografik detaylarını saklamak.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            address TEXT,
            occupation TEXT, -- Meslek
            availability_time TEXT, -- Müsaitlik saati (Örn: 18:00 sonrası)
            family_size INTEGER, -- Aile kişi sayısı
            age INTEGER, -- Yaş
            political_view TEXT, -- Politik görüş (Hassas veri)
            religious_view TEXT, -- Dini görüş (Hassas veri)
            notes TEXT, -- Diğer notlar (Hobiler vb.)
            birthdate TEXT, -- Doğum tarihi (YYYY-MM-DD)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            -- --- İletişim Merkezi Geliştirmeleri ---
            category TEXT DEFAULT 'general' NOT NULL, -- 'lead', 'client', 'tenant', 'partner', 'other'
            source_table TEXT, -- 'leads', 'users', 'parties' vb.
            source_id INTEGER, -- Kaynak tablodaki orijinal ID
            tags TEXT, -- JSON formatında etiketler ["yatirimci", "acil_ihtiyac"]
            UNIQUE(source_table, source_id)
        )
    ''')
    
    # --- Plan 5: 360 Degree Customer View (L-Metrics) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            url TEXT,
            event_type TEXT, -- scroll, click, focus, stay
            element_id TEXT,
            value TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_interactions_session ON user_interactions(session_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_interactions_type ON user_interactions(event_type)')

    # (staff_locations table moved/consolidated)
    # -----------------------------------------------------------------------

    # 7. Yeni Tablo: listings_shadow (Eklenti Veri Havuzu)
    #    - Amaç: Tarayıcı eklentisinden gelen ilan verilerini (Shadow Mode) saklamak.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings_shadow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            price_numeric REAL,
            estimated_rent REAL,
            roi_score REAL,
            amortization_years REAL,
            city TEXT,
            district TEXT,
            neighborhood TEXT,
            latitude REAL,
            longitude REAL,
            url TEXT UNIQUE,
            source TEXT, -- 'sahibinden', 'hepsiemlak'
            listing_type TEXT, -- 'Satılık', 'Kiralık'
            owner_name TEXT,
            owner_phone TEXT,
            listing_date TEXT,
            data_json TEXT, -- Tüm ham veri
            last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Mevcut tabloya yeni kolonları ekle (Migration desteği)
    columns_to_add = [
        ('price_numeric', 'REAL'),
        ('estimated_rent', 'REAL'),
        ('roi_score', 'REAL'),
        ('amortization_years', 'REAL'),
        ('city', 'TEXT'),
        ('district', 'TEXT'),
        ('neighborhood', 'TEXT'),
        ('latitude', 'REAL'),
        ('longitude', 'REAL'),
        ('listing_type', 'TEXT'),
        ('owner_name', 'TEXT'),
        ('owner_phone', 'TEXT'),
        ('listing_date', 'TEXT')
    ]
    for col_name, col_type in columns_to_add:
        try:
            cursor.execute(f'ALTER TABLE listings_shadow ADD COLUMN {col_name} {col_type}')
        except sqlite3.OperationalError:
            pass # Kolon zaten varsa hata verir, görmezden gel

    # --- LEADS TABLOSUNA PIPELINE_STAGE_ID EKLE (Migration) ---
    try:
        cursor.execute('ALTER TABLE leads ADD COLUMN pipeline_stage_id INTEGER REFERENCES pipeline_stages(id)')
    except sqlite3.OperationalError:
        pass

    # --- PAZARLAMA OTOMASYONU VE KAMPANYA TABLOLARI (Plan 2) ---

    # 8. Otomasyon Kuralları (HATA-003)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS automations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            trigger_event TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            last_run TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 9. Otomasyon Kayıtları
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS automation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER,
            lead_id INTEGER,
            action_taken TEXT,
            status TEXT DEFAULT 'success',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(rule_id) REFERENCES automation_rules(id),
            FOREIGN KEY(lead_id) REFERENCES leads(id)
        )
    ''')

    # 10. Kampanyalar (Marketing Automation)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            content_html TEXT NOT NULL,
            target_audience TEXT NOT NULL, -- 'all', 'vip', 'leads'
            campaign_type TEXT DEFAULT 'newsletter',
            created_by INTEGER,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(created_by) REFERENCES users(id)
        )
    ''')

    # 11. Kampanya Gönderim Kayıtları
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS campaign_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campaign_id INTEGER,
            recipient_email TEXT NOT NULL,
            status TEXT DEFAULT 'sent', -- sent, failed, opened
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(campaign_id) REFERENCES campaigns(id)
        )
    ''')

    # -----------------------------------------------------------------------

    # Personel Harcamaları (Expenses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL, -- Harcamayı yapan personel
            category TEXT, -- 'yemek', 'yakıt', 'temsil', 'kırtasiye'
            amount REAL NOT NULL,
            description TEXT,
            receipt_image TEXT, -- Fiş/Fatura görseli URL
            date TEXT,
            status TEXT DEFAULT 'pending', -- pending, approved, rejected
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Personel Mesai Yönetimi (Shift Management)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_shifts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            day_of_week INTEGER NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            is_off INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Komisyon / Hakediş Tablosu
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS commissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            contract_id INTEGER,
            amount REAL NOT NULL,
            rate REAL,
            description TEXT,
            month TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(contract_id) REFERENCES contracts(id)
        )
    ''')

    # Çoklu Platform Entegrasyon Merkezi
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS platform_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            platform_type TEXT NOT NULL,
            display_name TEXT,
            api_key TEXT,
            api_secret TEXT,
            access_token TEXT,
            account_url TEXT,
            status TEXT DEFAULT 'manual',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS publications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            platform_id INTEGER,
            platform_name TEXT NOT NULL,
            content_type TEXT,
            generated_text TEXT,
            listing_url TEXT,
            status TEXT DEFAULT 'draft',
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(platform_id) REFERENCES platform_connections(id)
        )
    ''')

    # Gelen Evraklar / Manuel Aktarım (Inbox)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS incoming_docs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, -- 'whatsapp', 'email', 'telegram', 'eldentesslim'
            sender TEXT, -- Gönderen kişi (Ortak Ali, Müşteri Ayşe vb.)
            file_path TEXT, -- Varsa dosya yolu
            file_type TEXT, -- 'pdf', 'image', 'text'
            content TEXT, -- Mesaj içeriği veya not
            status TEXT DEFAULT 'new',
            pipeline_stage_id INTEGER, -- new, reviewed, archived
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Alım Gücü Hesaplamaları (Purchasing Power)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchasing_power (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER, -- Hesaplamayı yapan
            cash_amount REAL DEFAULT 0,
            credit_amount REAL DEFAULT 0,
            barter_total REAL DEFAULT 0,
            total_power REAL DEFAULT 0,
            details_json TEXT, -- Araç/Mülk detayları JSON olarak
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # --- E-Posta Pazarlama ve İletişim Merkezi (Madde 6) ---
    
    # İmza Mahalle / Esnaf Modülü
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL, -- 'Tesisatçı', 'Restoran', 'Market', 'Kuru Temizleme'
            description TEXT,
            phone TEXT,
            address TEXT,
            logo_url TEXT,
            rating REAL DEFAULT 0.0,
            is_approved BOOLEAN DEFAULT 1, -- İmza onayı
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Komşuluk Duvarı (Neighborhood Wall) Gönderileri
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neighborhood_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL, -- 'duyuru', 'ulasim', 'paylasim', 'yardim'
            content TEXT NOT NULL,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Mahalle Talepleri (Neighborhood Demands)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS neighborhood_demands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL, -- 'Gayrimenkul', 'Hizmet', 'Organizasyon', 'Diger'
            content TEXT NOT NULL,
            user_name TEXT,
            user_phone TEXT,
            status TEXT DEFAULT 'open', -- 'open', 'in_progress', 'resolved'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Proje Landing Page (Tanıtım Sayfaları)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL, -- URL için (örn: vadi-evleri)
            name TEXT NOT NULL,
            description TEXT,
            hero_image_url TEXT, -- Kapak fotoğrafı
            theme_color TEXT DEFAULT '#000000', -- Altın/Siyah veya özel renk
            features JSON, -- "Havuz", "Güvenlik", "Kapalı Otopark" vb. JSON listesi
            price_range TEXT,
            location TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Proje Talepleri (Leads)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            message TEXT,
            status TEXT DEFAULT 'new',
            pipeline_stage_id INTEGER, -- 'new', 'contacted', 'closed'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
    ''')
    
    
    # (automation_rules already defined above at line 567)

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            type TEXT NOT NULL, -- 'pipeline', 'ai_alert', 'automation', 'system'
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'unread', -- 'unread', 'read'
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # --- PERFORMANS INDEKSLERI (ÖNERİ-007) ---
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_portfoyler_koleksiyon ON portfoyler(koleksiyon)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_portfoyler_fiyat ON portfoyler(fiyat)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_portfoyler_owner ON portfoyler(owner_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_segment ON leads(segment)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_assigned_user ON leads(assigned_user_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_username ON users(username)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_audit_created ON audit_logs(created_at)')

    # --- Audit Logs (ÖNERİ-006) ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS audit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            entity_id TEXT,
            user_id INTEGER,
            old_data JSON,
            new_data JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    
    # Use bcrypt for passwords (Modern Security Standard)
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    hashed_pw = bcrypt.hash(admin_password)
    
    # Insert default admin user if not exists
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?,?,?)', ('admin', hashed_pw, 'admin'))
    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar başarıyla oluşturuldu.")

def doldur_ornek_veriler():
    """Populates the database with example users, portfolios, hero slides, and appointments."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Yeni Örnek Kullanıcılar Ekle (Rol Testleri İçin)
    def get_hashed(pw):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pw.encode('utf-8'), salt).decode('utf-8')

    example_users = [
        ("admin", get_hashed("admin123"), "admin"),
        ("asistan", get_hashed("asistan123"), "employee"),
        ("muteahhit", get_hashed("test1234"), "contractor"),
        ("m_sahibi", get_hashed("test1234"), "owner"),
        ("kiraci", get_hashed("test1234"), "tenant"),
        ("partner_ajans", get_hashed("test1234"), "partner"),
    ]

    for un, pw, rl in example_users:
        cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?, ?, ?)', (un, pw, rl))
    
    # Test Sözleşmeleri (contracts) - Assuming user_id 5 exists for 'kiraci'
    # Note: The property_id '51c238b1-381f-49b0-9f5b-59ddbd9fe8ef' is not in the example portfoyler data.
    # This might cause a foreign key constraint error if not handled.
    # For demonstration, we'll use an existing property_id from portfoyler.
    # Let's use 'bogaz-villa' for property_id and user_id 5 (kiraci)
    cursor.execute('INSERT OR IGNORE INTO contracts (property_id, user_id, start_date, end_date, type) VALUES (?, ?, ?, ?, ?)', 
                   ('bogaz-villa', 5, '2024-01-01', '2025-01-01', 'Kira Sözleşmesi'))

    # (Removed redundant table creations and fixed sample data to match consolidated schema)
    
    # Sample data for tracking (mock)
    cursor.execute("INSERT OR IGNORE INTO staff_locations (id, user_id, latitude, longitude, location_type) VALUES (1, 1, 41.1123, 29.0234, 'checkin')")
    cursor.execute("INSERT OR IGNORE INTO staff_locations (id, user_id, latitude, longitude, location_type) VALUES (2, 2, 41.1150, 29.0210, 'periodic')")

    # Sample data for Property Units (Using property_id from portfoyler)
    # Schema: (id, property_id, unit_number, floor, unit_type, area_sqm, status)
    cursor.execute("INSERT OR IGNORE INTO property_units (id, property_id, unit_number, floor, unit_type, area_sqm, status) VALUES (1, 'bogaz-villa', 'A-12', '1', 'Villa', 450.0, 'Dolu')")
    
    # Sample dues payments (Using property_unit_id and user_id=5 for 'kiraci')
    # Schema: (property_unit_id, user_id, amount, due_date, status, description)
    cursor.execute("INSERT OR IGNORE INTO dues_payments (property_unit_id, user_id, amount, due_date, status, description) VALUES (1, 5, 1250.0, '2026-03-01', 'Ödendi', 'Mart 2026 Aidatı')")
    cursor.execute("INSERT OR IGNORE INTO dues_payments (property_unit_id, user_id, amount, due_date, status, description) VALUES (1, 5, 1250.0, '2026-02-02', 'Ödendi', 'Şubat 2026 Aidatı')")

    # Sample apartment expenses (Using property_id from portfoyler)
    # Schema: (id, property_id, expense_type, amount, expense_date, description)
    cursor.execute("INSERT OR IGNORE INTO apartment_expenses (property_id, expense_type, amount, expense_date, description) VALUES ('bogaz-villa', 'Asansör Bakımı', 4500.0, '2026-03-10', 'A Blok asansör halat değişimi ve periyodik bakım.')")
    cursor.execute("INSERT OR IGNORE INTO apartment_expenses (property_id, expense_type, amount, expense_date, description, invoice_file) VALUES ('bogaz-villa', 'Bahçe Düzenleme', 2200.0, '2026-03-05', 'Bahar bakımı ve yeni çiçek ekimi.', 'https://images.unsplash.com/photo-1589156229687-496a31ad1d1f?q=80&w=400')")
    cursor.execute("INSERT OR IGNORE INTO apartment_expenses (property_id, expense_type, amount, expense_date, description, invoice_file) VALUES ('bogaz-villa', 'Aydınlatma Onarımı', 850.0, '2026-03-12', 'Binas giriş armatür değişimi.', 'https://images.unsplash.com/photo-1590216087343-c2229b352576?q=80&w=400')")

    # Sample Polls
    cursor.execute("INSERT OR IGNORE INTO apartment_polls (id, mahalle_id, title, description, options, expires_at) VALUES (1, 1, 'Dış Cephe Boyası', 'Binamızın dış cephesinin bu yaz boyanmasını istiyor musunuz?', '[\"Evet, boyansın\", \"Hayır, seneye kalsın\", \"Sadece balkonlar\"]', '2026-04-15 00:00:00')")
    cursor.execute("INSERT OR IGNORE INTO apartment_polls (id, mahalle_id, title, description, options, expires_at) VALUES (2, 1, 'Otopark Düzenlemesi', 'Misafir araçları için ayrılan alanın genişletilmesi hakkında ne düşünüyorsunuz?', '[\"Genişletilsin\", \"Mevcut kalsın\", \"Ücretli olsun\"]', '2026-04-10 00:00:00')")
    print("Mesaj şablonları kontrol ediliyor...")
    cursor.execute('SELECT COUNT(*) FROM message_templates')
    if cursor.fetchone()[0] == 0:
        templates = [
            ('yatirimci', 'general', "Selamlar {name} Bey/Hanım, piyasada şu an nakit alımlarda ciddi fırsatlar oluşmaya başladı. Sizin yatırım kriterlerinize uyan 2-3 yer var, ne zaman müsait olursunuz?"),
            ('butce_odakli', 'property', "Merhaba {name}, bütçe planlamanızı konuşmuştuk. Bu portföy ({property_price}) krediye uygun ve pazarlık payı var. Görmek ister misiniz?"),
            ('butce_odakli', 'general', "Merhaba {name}, faiz oranlarıyla ilgili yeni bir kampanya duyumu aldık. Ev sahibi olma planınızı tekrar değerlendirmek isterseniz detayları paylaşabilirim."),
            ('yasam_tarzi', 'property', "{name} Hanım/Bey merhaba, tam aradığınız gibi 'huzurlu' bir yer buldum. {property_title} manzarası ve bahçesi sizi çok etkileyecek."),
            ('yasam_tarzi', 'general', "Merhaba {name}, yaşam standartlarınıza uygun, özellikle sosyal alanları güçlü yeni portföylerimiz geldi. Kahveye bekleriz :)"),
            ('buyuk_balik', 'property', "{name} Bey, rahatsız etmek istemedim. Sadece portföyümüze giren bu özel mülkü ({property_location}) piyasaya duyurmadan önce size sunmak istedim."),
            ('buyuk_balik', 'general', "{name} Bey selamlar, umarım keyifler yerindedir. Sektörle ilgili size özel hazırladığımız kısa bir analiz raporu var, incelemek isterseniz gönderebilirim."),
            ('acil', 'property', "{name} Bey/Hanım, bu portföy çok hızlı gidecek gibi duruyor. Fiyatı {property_price}. İlgileniyorsanız hemen randevu oluşturalım."),
            ('acil', 'general', "Merhaba {name}, acil satılık kategorisine düşen 2 yeni fırsat var. Henüz ilana girmedik, ilk siz görün istedim."),
            ('default', 'general', "Merhaba {name} Bey/Hanım, İmza Gayrimenkul'den ulaşıyorum. Size nasıl yardımcı olabilirim?")
        ]
        cursor.executemany('INSERT INTO message_templates (segment, context_type, template_text) VALUES (?, ?, ?)', templates)

    # Projeler (Landing Pages) Örnek Veri
    print("Örnek Proje verileri ekleniyor...")
    cursor.execute('SELECT COUNT(*) FROM projects')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO projects (slug, name, description, hero_image_url, theme_color, features, price_range, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'vadi-evleri', 
            'Vadi Evleri Premium', 
            'Doğanın kalbinde, lüks ve konforun buluştuğu eşsiz bir yaşam alanı. Şehrin gürültüsünden uzak ama merkeze sadece 15 dakika mesafede.', 
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?ixlib=rb-4.0.3&auto=format&fit=crop&w=2075&q=80', 
            '#b99860', 
            '["7/24 Güvenlik", "Açık Yüzme Havuzu", "Kapalı Otopark", "Akıllı Ev Sistemi", "Yerden Isıtma"]', 
            '15.000.000 TL - 25.000.000 TL', 
            'Zekeriyaköy, İstanbul'
        ))

    # Hero Slides Varsayılan Veriler
    print("Örnek Hero Slide verileri ekleniyor...")
    cursor.execute('SELECT COUNT(*) FROM hero_slides')
    if cursor.fetchone()[0] == 0:
        hero_ornekler = [
            ("https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=2000&q=80", 
             "Premium Yatırım Çözümleri", "Sadece Bir Ev Değil,", "Yeni Bir Hayat.", 
             "Detaylı Arama Yap", "Koleksiyonları Keşfet", "javascript:void(0)", 1),
             
            ("https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=2000&q=80", 
             "İmza Ayrıcalığı", "Geleceğinize", "Lüks Dokunuş.", 
             "Lüks Portföyler", "Yatırımları İncele", "arama.html", 2)
        ]
        cursor.executemany('''
            INSERT INTO hero_slides (resim_url, alt_baslik, baslik_satir1, baslik_satir2, buton1_metin, buton2_metin, buton2_link, sira) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', hero_ornekler)

    # Portfoyler
    print("Örnek portföy verileri ekleniyor...")
    portfoyler = [
        {
            "id": "bogaz-villa",
            "koleksiyon": "Prestij Koleksiyonu",
            "baslik1": "Boğaz Manzaralı",
            "baslik2": "Modern Villa",
            "lokasyon": "İstanbul, Sarıyer",
            "refNo": "IMZ-992",
            "fiyat": "₺35.000.000",
            "mahalle_id": "maslak",
            "oda": "6+2",
            "alan": "450 m²",
            "kat": "Müstakil",
            "ozellik_renk": "text-gold",
            "bg_renk": "bg-navy",
            "btn_renk": "bg-gold hover:bg-yellow-600 shadow-gold/20",
            "icon_renk": "border-gold",
            "resim_hero": "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=2000&q=80",
            "resim_hikaye": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
            "hikaye": "Sarıyer'in en prestijli noktasında, Boğaz'ın eşsiz maviliğine hakim bir konumda yükselen bu villa, modern mimariyle lüksün kusursuz uyumunu sunuyor. Her köşesinde en yüksek kalite malzemelerin kullanıldığı mülk, geniş pencereleri sayesinde günün her saati doğal ışıkla doluyor.",
            "ozellikler": json.dumps(["Akıllı Ev Sistemi", "Özel Isıtmalı Havuz", "4 Araçlık Otopark", "VRF İklimlendirme"]),
            "danisman_isim": "Selim Yıldırım",
            "danisman_unvan": "Danışman",
            "danisman_resim": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "ekolojik-ev",
            "koleksiyon": "Doğa Koleksiyonu",
            "baslik1": "Ekolojik",
            "baslik2": "Orman Evi",
            "lokasyon": "Bolu, Göynük",
            "refNo": "IMZ-101",
            "fiyat": "₺18.500.000",
            "oda": "4+1",
            "alan": "280 m²",
            "kat": "2 Katlı",
            "ozellik_renk": "text-natureLight",
            "bg_renk": "bg-navy",
            "btn_renk": "bg-natureLight hover:bg-green-700 shadow-natureLight/20",
            "icon_renk": "border-natureLight",
            "resim_hero": "https://images.unsplash.com/photo-1580587771525-78b9dba38a72?auto=format&fit=crop&w=2000&q=80",
            "resim_hikaye": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
            "hikaye": "Sapanca'nın en korunmuş ormanlarının kalbinde, doğal gölet manzarasına hakim bir konumda inşa edilen bu ekolojik orman evi, sürdürülebilir yaşamla lüksün kusursuz uyumunu sunuyor. Doğal ahşap ve taş mimarisi, yüksek kapasiteli güneş panelleri ve yağmur suyu hasat sistemleriyle doğaya %100 uyumlu.",
            "ozellikler": json.dumps(["Güneş Enerji Sistemi", "Doğal Yüzme Göleti", "Yağmur Suyu Hasadı", "Şömine & Akıllı Ev"]),
            "danisman_isim": "Burak Kaya",
            "danisman_unvan": "Doğa Koleksiyonu Direktörü",
            "danisman_resim": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?auto=format&fit=crop&w=300&q=80"
        },
        {
            "id": "cam-oda-penthouse",
            "koleksiyon": "Modern Koleksiyon",
            "baslik1": "Cam Oda",
            "baslik2": "Penthouse",
            "lokasyon": "İstanbul, Levent",
            "refNo": "IMZ-505",
            "fiyat": "₺42.000.000",
            "oda": "5+1",
            "alan": "350 m²",
            "kat": "42. Kat",
            "ozellik_renk": "text-modern",
            "bg_renk": "bg-navy",
            "btn_renk": "bg-modern hover:bg-teal-600 shadow-modern/20",
            "icon_renk": "border-modern",
            "resim_hero": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=2000&q=80",
            "resim_hikaye": "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
            "hikaye": "Şehrin ritmini en üst noktadan hissedin. 360 derece kesintisiz şehir manzarası sunan bu ultra lüks penthouse, akıllı bina teknolojileriyle donatılmıştır. Tavandan tabana cam cepheleri, şehrin tüm dinamizmini evinize davet ederken maksimum mahremiyet de sağlıyor.",
            "ozellikler": json.dumps(["360 Derece Teras", "Rezidans Hizmetleri", "Özel Asansör", "Gaggenau Mutfak"]),
            "danisman_isim": "Cemil Arslan",
            "danisman_unvan": "Modern Koleksiyon Direktörü",
            "danisman_resim": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=300&q=80"
        }
    ]
    
    for p in portfoyler:
        cursor.execute('''
            INSERT OR IGNORE INTO portfoyler (id, koleksiyon, baslik1, baslik2, lokasyon, refNo, fiyat, oda, alan, kat, ozellik_renk, bg_renk, btn_renk, icon_renk, resim_hero, resim_hikaye, hikaye, ozellikler, danisman_isim, danisman_unvan, danisman_resim)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (p['id'], p['koleksiyon'], p['baslik1'], p['baslik2'], p['lokasyon'], p['refNo'], p['fiyat'], p['oda'], p['alan'], p['kat'], p['ozellik_renk'], p['bg_renk'], p['btn_renk'], p['icon_renk'], p['resim_hero'], p['resim_hikaye'], p['hikaye'], p['ozellikler'], p['danisman_isim'], p['danisman_unvan'], p['danisman_resim']))
        
    print("Örnek ekip verileri ekleniyor...")
    ekip_uyeleri = [
        {
            "id": "ahmet-imza",
            "isim": "Ahmet İmza",
            "unvan": "Kurucu & CEO",
            "detaylar": json.dumps(["Lüks Konut Sektöründe 25 Yıllık Deneyim", "Sektör Öncüsü Vizyoner", "Sayısız Ödül ve Başarı"]),
            "uzmanlikAlanlari": json.dumps(["Stratejik Yönetim", "Lüks Proje Geliştirme", "Uluslararası Yatırım"]),
            "telefon": "+90 532 111 22 33",
            "email": "ahmet@imza.com",
            "resim": "https://images.unsplash.com/photo-1560250097-0b93528c311a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "yonetici"
        },
        {
            "id": "zeynep-yilmaz",
            "isim": "Zeynep Yılmaz",
            "unvan": "Operasyon Direktörü",
            "detaylar": json.dumps(["Müşteri İlişkileri Uzmanı", "Operasyonel Kurulum & Takip", "Kusursuz İş Akışı Tasarımı"]),
            "uzmanlikAlanlari": json.dumps(["Takım Yönetimi", "Müşteri Deneyimi Artırımı", "Operasyonel Optimizasyon"]),
            "telefon": "+90 532 222 33 44",
            "email": "zeynep@imza.com",
            "resim": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "yonetici"
        },
        {
            "id": "caner-demir",
            "isim": "Caner Demir",
            "unvan": "Satış Direktörü",
            "detaylar": json.dumps(["15 Yıllık Satış ve Pazarlama Lideri", "Geniş VIP Müşteri Ağı", "Risk ve Kriz Yönetimi Uzmanı"]),
            "uzmanlikAlanlari": json.dumps(["VIP Satış ve Pazarlama", "Portföy Yönetimi ve Analizi", "Risk Yönetimi"]),
            "telefon": "+90 532 333 44 55",
            "email": "caner@imza.com",
            "resim": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "yonetici"
        },
        {
            "id": "selim-yildirim",
            "isim": "Selim Yıldırım",
            "unvan": "Boğaz Hattı Uzmanı",
            "detaylar": json.dumps(["Yalı & Tarihi Eser Uzmanlığı", "Boğaziçi Sit Alanı Mevzuatı", "Restorasyon Süreç Takibi"]),
            "uzmanlikAlanlari": json.dumps(["Tarihi Yalılar", "Sit Alanı Danışmanlığı", "Lüks Konut Alım-Satım"]),
            "telefon": "+90 532 444 55 66",
            "email": "selim@imza.com",
            "resim": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "danisman"
        },
         {
            "id": "elif-aksoy",
            "isim": "Elif Aksoy",
            "unvan": "Rezidans ve Ticari Gayrimenkul",
            "detaylar": json.dumps(["A Sınıfı Ofisler ve Plazalar", "Residence ve Markalı Projeler", "Global Şirketler İrtibatı"]),
            "uzmanlikAlanlari": json.dumps(["Ticari Yatırımlar", "Kurumsal Kiralama", "Rezidans Satışları"]),
            "telefon": "+90 532 555 66 77",
            "email": "elif@imza.com",
            "resim": "https://images.unsplash.com/photo-1580489944761-15a19d654956?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "danisman"
        },
         {
            "id": "burak-kaya",
            "isim": "Burak Kaya",
            "unvan": "Doğa Koleksiyonu & Müstakil Evler",
            "detaylar": json.dumps(["Ekolojik Projeler Uzmanı", "Arsa Geliştirme ve Parselasyon", "Doğa Dostu Lüks Odaklı"]),
            "uzmanlikAlanlari": json.dumps(["Çiftlik ve Tarım Arazileri", "Sürdürülebilir Mimari Projeler", "Müstakil Yaşam Alanları"]),
            "telefon": "+90 532 666 77 88",
            "email": "burak@imza.com",
            "resim": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60",
            "sosyal_linkedin": "#",
            "sosyal_instagram": "#",
            "sosyal_twitter": "#",
            "tip": "danisman"
        }
    ]
    
    for e in ekip_uyeleri:
        cursor.execute('''
            INSERT OR IGNORE INTO ekip (id, isim, unvan, detaylar, uzmanlikAlanlari, telefon, email, resim, sosyal_linkedin, sosyal_instagram, sosyal_twitter, tip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (e['id'], e['isim'], e['unvan'], e['detaylar'], e['uzmanlikAlanlari'], e['telefon'], e['email'], e['resim'], e['sosyal_linkedin'], e['sosyal_instagram'], e['sosyal_twitter'], e['tip']))

    # --- Sözleşme Şablonları & Maddeleri (Örnek Veriler) ---
    print("Örnek sözleşme şablonları ekleniyor...")
    cursor.execute('SELECT COUNT(*) FROM contract_templates')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT OR IGNORE INTO contract_templates (name, description) VALUES (?, ?)', 
                       ("Konut Kira Sözleşmesi", "Standart konut kiralama işlemleri için kullanılır."))
        template_kira_id = cursor.lastrowid

        cursor.execute('INSERT OR IGNORE INTO contract_templates (name, description) VALUES (?, ?)', 
                       ("Gayrimenkul Satış Vaadi Sözleşmesi", "Satış vaadi ön protokolu gerektiren durumlarda kullanılır."))
        template_satis_id = cursor.lastrowid
        
        # Kira Maddeleri
        kira_maddeleri = [
            (template_kira_id, "Kira Bedeli ve Ödeme Şekli: Kiracı, aylık kira bedelini her ayın 1'i ile 5'i arasında mal sahibinin bildirdiği banka hesabına peşin olarak yatıracaktır.", True, 1),
            (template_kira_id, "Depozito: Kiracı, sözleşme imzalandığında 2 aylık kira bedeli tutarında depozitoyu nakit olarak teslim etmiştir.", True, 2),
            (template_kira_id, "Kullanım Amacı: Kiralanan mülk sadece mesken (konut) olarak kullanılabilir, ticari faaliyette bulunulamaz.", True, 3),
            (template_kira_id, "Alt Kiralama Yasağı: Kiracı, kiralanan mülkü kısmen veya tamamen başkasına kiralayamaz veya kullanım hakkını devredemez.", True, 4),
            (template_kira_id, "Aidat ve Giderler: Bina/Site aidatları, çevre temizlik vergisi ve kullanıma bağlı tüm giderler (elektrik, su, doğalgaz) kiracıya aittir.", False, 5),
            (template_kira_id, "Evcil Hayvan: Kiralanan mülkte evcil hayvan beslenmesi mal sahibinin yazılı iznine tabidir.", False, 6)
        ]
        
        cursor.executemany('INSERT INTO contract_clauses (template_id, clause_text, is_mandatory, sort_order) VALUES (?, ?, ?, ?)', kira_maddeleri)

        # Satış Vaadi Maddeleri
        satis_maddeleri = [
            (template_satis_id, "Satış Bedeli: Taraflar, söz konusu gayrimenkulün satışı için anlaşılan toplam bedeli nakden ve defaten ödemeyi taahhüt eder.", True, 1),
            (template_satis_id, "Cayma Bedeli ve Cezai Şart: Sözleşmeden haksız olarak cayan taraf, diğer tarafa anlaşılan bedelin %10'u oranında cezai şart ödemeyi kabul eder.", True, 2),
            (template_satis_id, "Tapu Devri: Tapu devir işlemleri, alıcının satış bedelinin tamamını ödediği gün ilgili Tapu Sicil Müdürlüğü'nde gerçekleştirilecektir.", True, 3),
            (template_satis_id, "Harçlar ve Masraflar: Tapu alım satım harçları ve döner sermaye masrafları taraflarca yarı yarıya / alıcı tarafından ödenecektir.", False, 4)
        ]

        cursor.executemany('INSERT INTO contract_clauses (template_id, clause_text, is_mandatory, sort_order) VALUES (?, ?, ?, ?)', satis_maddeleri)

    # Örnek taraflar
    sample_parties = [
        {
            'tc_no': '12345678901',
            'vkn': None,
            'party_type': 'individual',
            'name': 'Ali Demir',
            'phone': '5551234567',
            'email': 'ali.demir@example.com',
            'address': 'İstiklal Cad. No:10, Beyoğlu, İstanbul'
        },
        {
            'tc_no': None,
            'vkn': '9876543210',
            'party_type': 'corporate',
            'name': 'ABC İnşaat A.Ş.',
            'phone': '2125555555',
            'email': 'info@abcinsaat.com.tr',
            'address': 'Levent Mah. Sanayi Cad. No:25, Beşiktaş, İstanbul'
        }
    ]
    
    # Taraf verilerini ekle
    for party in sample_parties:
        cursor.execute('''
            INSERT OR IGNORE INTO parties (tc_no, vkn, party_type, name, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            party['tc_no'],
            party['vkn'],
            party['party_type'],
            party['name'],
            party['phone'],
            party['email'],
            party['address']
        ))

    # Örnek Esnaflar (İmza Mahalle)
    print("Örnek esnaf verileri ekleniyor...")
    cursor.execute('SELECT COUNT(*) FROM businesses')
    if cursor.fetchone()[0] == 0:
        sample_businesses = [
            ('Sarıyer Tesisat', 'Tesisatçı', '7/24 acil tesisat hizmetleri, garantili onarım.', '05321234567', 'Sarıyer Merkez Mah. No: 12', 'https://placehold.co/100x100/0a192f/c5a059?text=ST', 4.8, 1),
            ('Levent Fırın', 'Fırın', 'Sıcak simit, poğaça ve özel ekşi mayalı ekmekler.', '02122801020', 'Levent, Çarşı Cad. No: 5', 'https://placehold.co/100x100/c5a059/0a192f?text=LF', 4.9, 1),
            ('Bebek Balıkçısı', 'Restoran', 'Boğaz manzarası eşliğinde taze deniz ürünleri.', '02122635588', 'Bebek Sahili, No: 44', 'https://placehold.co/100x100/e17055/ffffff?text=BB', 4.5, 0),
            ('İmza Kuru Temizleme', 'Kuru Temizleme', 'Hassas kumaşlar için özel kuru temizleme ve ütü hizmeti.', '08503051010', 'Maslak, Ataşehir Sok. No: 1', 'https://placehold.co/100x100/1b4d3e/ffffff?text=IKT', 5.0, 1)
        ]
        cursor.executemany('''
            INSERT INTO businesses (name, category, description, phone, address, logo_url, rating, is_approved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_businesses)

    conn.commit()
    conn.close()

class AuditLogger:
    @staticmethod
    def log(action, entity_type, entity_id, user_id, old_data=None, new_data=None):
        try:
            conn = sqlite3.connect(DB_NAME)
            conn.execute('''
                INSERT INTO audit_logs (action, entity_type, entity_id, user_id, old_data, new_data)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (action, entity_type, entity_id, user_id, 
                  json.dumps(old_data) if old_data else None, 
                  json.dumps(new_data) if new_data else None))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Audit Log Hatası: {e}")

if __name__ == "__main__":
    init_db()
    doldur_ornek_veriler()
