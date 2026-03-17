from flask import Blueprint, request, jsonify
from database import get_db_connection
import json
import re
from functools import wraps
from urllib.parse import urlparse

tracking_bp = Blueprint('tracking', __name__)

def token_required(f):
    """
    Token doğrulama decorator'ı
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'error': 'Token bulunamadı!'}), 401
        if not token:
            return jsonify({'error': 'Token gerekli!'}), 401
        
        # Burada gerçek token doğrulama yapılmalı
        # Şimdilik basit bir kontrol yapıyoruz
        if token != "test_token":
            return jsonify({'error': 'Geçersiz token!'}), 401
            
        return f(*args, **kwargs)
    return decorated

@tracking_bp.route('/api/track', methods=['POST'])
def track_event():
    data = request.json
    session_id = data.get('session_id')
    event_type = data.get('event_type') # 'page_view', 'tool_usage', 'click'
    page_url = data.get('page_url')
    meta_data = data.get('meta_data', {})
    
    if not session_id:
        return jsonify({'status': 'ignored'}), 200

    conn = get_db_connection()
    try:
        # Etkileşimi kaydet
        conn.execute('''
            INSERT INTO lead_interactions (session_id, tool_name, data_json)
            VALUES (?, ?, ?)
        ''', (session_id, event_type, json.dumps({'url': page_url, 'meta': meta_data})))
        conn.commit()
        return jsonify({'status': 'tracked'}), 201
    finally:
        conn.close()

@tracking_bp.route('/api/tracking/sync', methods=['POST'])
def sync_metrics():
    data = request.json
    shadow_id = data.get('shadow_id')
    metrics = data.get('metrics', {})
    geo = data.get('geo', {})
    
    if not shadow_id:
        return jsonify({'error': 'Missing shadow_id'}), 400

    conn = get_db_connection()
    try:
        # Ziyaretçi senkronizasyonu (JSON formatında saklama)
        conn.execute('''
            INSERT INTO lead_interactions (session_id, tool_name, data_json)
            VALUES (?, ?, ?)
        ''', (shadow_id, 'L-Metrics Sync', json.dumps({
            'metrics': metrics,
            'geo': geo,
            'url': request.referrer
        })))
        conn.commit()
        return jsonify({'status': 'synced'}), 201
    finally:
        conn.close()

@tracking_bp.route('/api/staff/location', methods=['POST'])
def track_staff_location():
    """
    Personel konum takibi için endpoint
    """
    data = request.json
    user_id = data.get('user_id')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    accuracy = data.get('accuracy')
    location_type = data.get('location_type', 'checkin')
    notes = data.get('notes')
    
    if not all([user_id, latitude, longitude]):
        return jsonify({'error': 'Missing required fields: user_id, latitude, longitude'}), 400

    conn = get_db_connection()
    try:
        conn.execute('''
            INSERT INTO staff_locations (user_id, latitude, longitude, accuracy, location_type, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, latitude, longitude, accuracy, location_type, notes))
        conn.commit()
        return jsonify({'status': 'Location tracked successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@tracking_bp.route('/api/tracking/location', methods=['POST'])
@token_required
def track_user_location():
    """
    Mobil uygulama için konum takibi endpoint'i
    """
    try:
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        auto = data.get('auto', False)
        
        if not all([latitude, longitude]):
            return jsonify({'error': 'Enlem ve boylam bilgisi gerekli'}), 400

        user_id = "mobile_user"
        
        conn = get_db_connection()
        try:
            conn.execute('''
                INSERT INTO staff_locations (user_id, latitude, longitude, location_type, notes)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, latitude, longitude, 'mobile', f'Otomatik gönderim: {auto}' if auto else 'Manuel gönderim'))
            conn.commit()
            return jsonify({'status': 'Konum başarıyla kaydedildi'}), 201
        except Exception as e:
            return jsonify({'error': f'Veritabanı hatası: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'İstek işlenirken hata oluştu: {str(e)}'}), 500

@tracking_bp.route('/api/extension/sync', methods=['POST'])
def sync_extension_data():
    """
    Tarayıcı eklentisinden gelen ilan verilerini (Shadow Mode) kaydeder.
    """
    try:
        data = request.json
        title = data.get('title')
        price = data.get('price')
        url = data.get('url')
        
        # Yeni Alanlar
        city = data.get('city')
        district = data.get('district')
        neighborhood = data.get('neighborhood')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        # Arbitraj & Eşleştirme Alanları
        owner_name = data.get('owner_name')
        owner_phone = data.get('owner_phone')
        listing_date = data.get('listing_date')
        
        if not url:
            return jsonify({'error': 'URL bilgisi gerekli'}), 400

        # --- ROI & Amortisman Hesaplama ---
        price_numeric = 0
        if price:
            # Sadece sayıları al (Örn: "1.500.000 TL" -> 1500000)
            price_numeric = float(re.sub(r'[^\d]', '', str(price)) or 0)

        listing_type = data.get('listing_type', 'Satılık')
        estimated_rent = 0
        roi_score = 0
        amortization_years = 0

        conn = get_db_connection()
        try:
            if listing_type == 'Satılık' and price_numeric > 0:
                # Bölgesel kira ortalamasını bul (Aggregated Data)
                # 1. Kendi mahallesindeki kira ilanlarının ortalaması
                avg_rent = conn.execute('''
                    SELECT AVG(price_numeric) FROM listings_shadow 
                    WHERE listing_type = 'Kiralık' AND district = ? AND neighborhood = ? AND price_numeric > 0
                ''', (district, neighborhood)).fetchone()[0]
                
                # 2. Mahallede veri yoksa ilçe ortalaması
                if not avg_rent:
                    avg_rent = conn.execute('''
                        SELECT AVG(price_numeric) FROM listings_shadow 
                        WHERE listing_type = 'Kiralık' AND district = ? AND price_numeric > 0
                    ''', (district,)).fetchone()[0]
                
                # 3. Hala veri yoksa 1/240 çarpanı (Muhafazakar model)
                if not avg_rent:
                    estimated_rent = price_numeric / 240
                else:
                    estimated_rent = float(avg_rent)
                
                annual_rent = estimated_rent * 12
                roi_score = (annual_rent / price_numeric) * 100
                amortization_years = price_numeric / annual_rent
            elif listing_type == 'Kiralık':
                estimated_rent = price_numeric # Kiralık ilan için fiyatın kendisi tahmini kiradır

            # URL'den site adını (source) dinamik ayıkla
            parsed_url = urlparse(url)
            domain = parsed_url.netloc.replace('www.', '').split('.')[0]
            source = domain if domain else 'other'
            # İlanı kaydet veya güncelle
            conn.execute('''
                INSERT INTO listings_shadow (
                    title, price, price_numeric, estimated_rent, 
                    roi_score, amortization_years,
                    city, district, neighborhood, 
                    latitude, longitude, url, source, listing_type, 
                    owner_name, owner_phone, listing_date, data_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    title=excluded.title,
                    price=excluded.price,
                    price_numeric=excluded.price_numeric,
                    estimated_rent=excluded.estimated_rent,
                    roi_score=excluded.roi_score,
                    amortization_years=excluded.amortization_years,
                    city=excluded.city,
                    district=excluded.district,
                    neighborhood=excluded.neighborhood,
                    latitude=excluded.latitude,
                    longitude=excluded.longitude,
                    listing_type=excluded.listing_type,
                    owner_name=excluded.owner_name,
                    owner_phone=excluded.owner_phone,
                    listing_date=excluded.listing_date,
                    data_json=excluded.data_json,
                    last_seen_at=CURRENT_TIMESTAMP
            ''', (
                title, price, price_numeric, estimated_rent, 
                roi_score, amortization_years,
                city, district, neighborhood, 
                latitude, longitude, url, source, listing_type,
                owner_name, owner_phone, listing_date, json.dumps(data)
            ))
            conn.commit()
            return jsonify({'status': 'Success', 'message': 'İlan verisi senkronize edildi'}), 201
        except Exception as e:
            return jsonify({'error': f'Veritabanı hatası: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'İstek işlenirken hata oluştu: {str(e)}'}), 500

@tracking_bp.route('/api/extension/listings', methods=['GET'])
def get_extension_listings():
    """
    Eklentiden gelen tüm shadow ilanları listeler.
    """
    conn = get_db_connection()
    try:
        listings = conn.execute('SELECT * FROM listings_shadow ORDER BY last_seen_at DESC').fetchall()
        return jsonify([dict(row) for row in listings]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@tracking_bp.route('/api/tracking/interactions', methods=['GET'])
def get_interactions():
    """
    Kendi sitemizdeki kullanıcı etkileşimlerini (L-Metrics) listeler.
    """
    conn = get_db_connection()
    try:
        # En son etkileşimleri getir
        interactions = conn.execute('''
            SELECT * FROM lead_interactions 
            ORDER BY created_at DESC 
            LIMIT 200
        ''').fetchall()
        return jsonify([dict(row) for row in interactions]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()
