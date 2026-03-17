from flask import Blueprint, request, jsonify
from database import get_db_connection
import json
from functools import wraps

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
        
        if not url:
            return jsonify({'error': 'URL bilgisi gerekli'}), 400

        source = 'sahibinden' if 'sahibinden.com' in url else 'hepsiemlak' if 'hepsiemlak.com' in url else 'other'
        
        conn = get_db_connection()
        try:
            # İlanı kaydet veya güncelle
            conn.execute('''
                INSERT INTO listings_shadow (
                    title, price, city, district, neighborhood, 
                    latitude, longitude, url, source, data_json
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    title=excluded.title,
                    price=excluded.price,
                    city=excluded.city,
                    district=excluded.district,
                    neighborhood=excluded.neighborhood,
                    latitude=excluded.latitude,
                    longitude=excluded.longitude,
                    data_json=excluded.data_json,
                    last_seen_at=CURRENT_TIMESTAMP
            ''', (title, price, city, district, neighborhood, latitude, longitude, url, source, json.dumps(data)))
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
