# Saha Operasyonları Modülü - Geliştirme Durumu

Saha verimliliğini artıran GPS ve denetim odaklı modüldür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **GPS Takip Sistemi:** `api/tracking.py` ile personel konumunun periyodik kaydı.
- [x] **Dijital Denetim Formu:** `property_inspections` tablosu ve interaktif kontrol listesi UI.
- [x] **Ziyaret History (Playback):** Geçmiş rotaların harita üzerinde izlenebilmesi.

## Teknik Altyapı
- **Backend:** `api/tracking.py` ve `api/inspection.py`.
- **Frontend:** Leaflet.js (Harita takibi için) ve Custom Checklist UI.
- **Veritabanı:** `staff_locations`, `property_inspections` tabloları.

## Gelecek Planları
- [ ] **Çevrimdışı (Offline) Denetim:** İnternet çekmeyen bölgelerde denetim yapıp sonra senkronize etme.
- [ ] **Rota Optimizasyonu:** Danışman için en verimli ziyaret rotasını çizen AI motoru.