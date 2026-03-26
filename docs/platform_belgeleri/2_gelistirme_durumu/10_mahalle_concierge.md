# Mahalle Concierge Modülü - Geliştirme Durumu

Yaşam OS vizyonunun en interaktif modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Haftalık Takvim UI:** `api/neighborhood.py` - Rezervasyonlar için görsel takvim altyapısı.
- [x] **Hizmet Talep Sistemi:** Arıza/Bakım taleplerinin yönetimi.
- [x] **Esnaf Entegrasyonu:** `neighborhood_facilities` tablosunda kategori bazlı liste.

## Teknik Altyapı
- **Backend:** Flask Blueprint (`neighborhood_bp`).
- **Veritabanı:** `service_requests`, `facility_bookings` tabloları.

## Gelecek Planları
- [ ] **Gerçek Zamanlı GPS Shuttle:** Servis araçlarına takılacak GPS modülü ile haritada canlı izleme.
- [ ] **Sesli Komut Entegrasyonu:** (Siri/Alexa üzerinden rezervasyon yapabilme).