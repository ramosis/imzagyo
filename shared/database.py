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

DB_URL = os.environ.get("DATABASE_URL", "data/imza_database.db")
# Normalize path (remove sqlite:/// used in CI)
DB_NAME = DB_URL.replace("sqlite:///", "").replace("sqlite://", "")
if not DB_NAME or DB_NAME == ":memory:":
    DB_NAME = ":memory:"

def get_db_connection():
    """Returns a sqlite3 connection object with row_factory set to Row."""
    if DB_NAME != ":memory:":
        os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)
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

    # Ensure PRAGMA foreign_keys = ON is set
    conn = get_db_connection()
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
            baslik1_en TEXT,
            baslik1_ar TEXT,
            baslik2_en TEXT,
            baslik2_ar TEXT,
            lokasyon_en TEXT,
            lokasyon_ar TEXT,
            hikaye_en TEXT,
            hikaye_ar TEXT,
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

    # Dil Sütunları
    for col in ['baslik1_en', 'baslik1_ar', 'baslik2_en', 'baslik2_ar', 'lokasyon_en', 'lokasyon_ar', 'hikaye_en', 'hikaye_ar']:
        try:
            cursor.execute(f'ALTER TABLE portfoyler ADD COLUMN {col} TEXT')
        except sqlite3.OperationalError:
            pass

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
            contract_type TEXT NOT NULL,
            description TEXT,
            html_template TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_default BOOLEAN DEFAULT 0
        )
    ''')

    # Sözleşme Maddeleri (Clauses)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract_clauses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            clause_type TEXT,
            usage_count INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 10. CONTRACTS & PARTIES (Section 3.10)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_number TEXT UNIQUE NOT NULL,
            contract_type TEXT NOT NULL,
            status TEXT DEFAULT 'draft',
            property_id TEXT,
            lead_id INTEGER,
            landlord_id INTEGER,
            tenant_id INTEGER,
            buyer_id INTEGER,
            seller_id INTEGER,
            price REAL NOT NULL,
            currency TEXT DEFAULT 'TRY',
            commission_rate REAL DEFAULT 0.0,
            commission_amount REAL DEFAULT 0.0,
            start_date TEXT,
            end_date TEXT,
            signing_date TEXT,
            template_id INTEGER,
            content TEXT,
            content_json TEXT,
            is_signed BOOLEAN DEFAULT 0,
            signed_by_landlord BOOLEAN DEFAULT 0,
            signed_by_tenant BOOLEAN DEFAULT 0,
            signed_by_buyer BOOLEAN DEFAULT 0,
            signed_by_seller BOOLEAN DEFAULT 0,
            signature_data TEXT,
            created_by INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contract_clause_links (
            contract_id INTEGER,
            clause_id INTEGER,
            PRIMARY KEY (contract_id, clause_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prepared_contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            pdf_path TEXT,
            pdf_url TEXT,
            status TEXT DEFAULT 'prepared',
            sent_to TEXT,
            sent_at TIMESTAMP,
            viewed_at TIMESTAMP,
            signed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Taraflar (Müşteriler, Satıcılar vb.)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parties (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            contract_id INTEGER NOT NULL,
            party_type TEXT NOT NULL,
            full_name TEXT NOT NULL,
            tc_no TEXT,
            phone TEXT,
            email TEXT,
            address TEXT,
            is_signed BOOLEAN DEFAULT 0,
            signed_at TIMESTAMP,
            signature_ip TEXT
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

    # DEPRECATED: contracts table is now handled in Section 3.10 above.
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

        -- System Settings Table for configurable options
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                category TEXT,
                description TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        -- Seed default storage settings
        cursor.execute("INSERT OR IGNORE INTO system_settings (key, value, category, description) VALUES ('storage_provider', 'local', 'storage', 'Provider for file storage (local, drive, cloud)')")
        cursor.execute("INSERT OR IGNORE INTO system_settings (key, value, category, description) VALUES ('upload_path', 'static/uploads/contracts', 'storage', 'Base path for contract related uploads')")


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

    conn.commit()
    
    # Use bcrypt for passwords (Modern Security Standard)
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    hashed_pw = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Insert default admin user if not exists
    cursor.execute('INSERT OR IGNORE INTO users (username, password_hash, role) VALUES (?,?,?)', ('admin', hashed_pw, 'admin'))
    
    conn.commit()
    conn.close()
    print("Veritabanı ve tablolar başarıyla oluşturuldu.")

def doldur_ornek_veriler():
    """Populates the database with example users, portfolios, hero slides, and appointments."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. USERS (Independent)
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
    
    # 2. PORTFOYLER (Independent)
    print("Örnek portföy verileri ekleniyor...")
    portfoyler = [
        {
            "id": "bogaz-villa",
            "koleksiyon": "Prestij Koleksiyonu",
            "baslik1": "Boğaz Manzaralı",
            "baslik2": "Modern Villa",
            "lokasyon": "İstanbul, Sarıyer",
            "refNo": "IMZ-992",
            "fiyat": 35000000.0,
            "oda": "6+2",
            "alan": "450 m²",
            "kat": "Müstakil",
            "ozellik_renk": "text-gold",
            "bg_renk": "bg-navy",
            "btn_renk": "bg-gold hover:bg-yellow-600 shadow-gold/20",
            "icon_renk": "border-gold",
            "resim_hero": "https://images.unsplash.com/photo-1613977257363-707ba9348227?auto=format&fit=crop&w=2000&q=80",
            "resim_hikaye": "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80",
            "hikaye": "Sarıyer'in en prestijli noktasında...",
            "ozellikler": json.dumps(["Akıllı Ev Sistemi", "Özel Isıtmalı Havuz"]),
            "danisman_isim": "Selim Yıldırım",
            "danisman_unvan": "Danışman",
            "danisman_resim": "https://images.unsplash.com/photo-1560250097-0b93528c311a?auto=format&fit=crop&w=300&q=80"
        }
    ]
    for p in portfoyler:
        cursor.execute('''
            INSERT OR IGNORE INTO portfoyler (id, koleksiyon, baslik1, baslik2, lokasyon, refNo, fiyat, oda, alan, kat, ozellik_renk, bg_renk, btn_renk, icon_renk, resim_hero, resim_hikaye, hikaye, ozellikler, danisman_isim, danisman_unvan, danisman_resim)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (p['id'], p['koleksiyon'], p['baslik1'], p['baslik2'], p['lokasyon'], p['refNo'], p['fiyat'], p['oda'], p['alan'], p['kat'], p['ozellik_renk'], p['bg_renk'], p['btn_renk'], p['icon_renk'], p['resim_hero'], p['resim_hikaye'], p['hikaye'], p['ozellikler'], p['danisman_isim'], p['danisman_unvan'], p['danisman_resim']))

    # 1.5 CONTRACT TEMPLATES (Crucial for service logic)
    cursor.execute('''
        INSERT OR IGNORE INTO contract_templates (name, contract_type, html_template, is_default)
        VALUES (?, ?, ?, ?)
    ''', ('Standart Kiralama', 'kiralama', '<h1>Kiralama Sözleşmesi</h1><p>Mülk: {{ property_id }}</p>', 1))

    # 3. CONTRACTS (Dependent on Users & Portfoyler)
    # user_id 5 should be 'kiraci' if we inserted in order and it's a fresh DB
    # 10. CONTRACTS (Standardized)
    cursor.execute('''
        INSERT OR IGNORE INTO contracts (
            contract_number, contract_type, property_id, price, 
            start_date, end_date, created_by, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('IMZ-2024-00001', 'kiralama', 'bogaz-villa', 150000.0, '2024-01-01', '2025-01-01', 5, 'active'))

    # 4. REMAINING (Simplified for stability)
    cursor.execute("INSERT OR IGNORE INTO property_units (id, property_id, unit_number, floor, unit_type, area_sqm, status) VALUES (1, 'bogaz-villa', 'A-12', '1', 'Villa', 450.0, 'Dolu')")
    cursor.execute("INSERT OR IGNORE INTO dues_payments (property_unit_id, user_id, amount, due_date, status, description) VALUES (1, 5, 1250.0, '2026-03-01', 'Ödendi', 'Mart 2026 Aidatı')")
    
    conn.commit()
    conn.close()
    print("Example data seeded successfully.")

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
