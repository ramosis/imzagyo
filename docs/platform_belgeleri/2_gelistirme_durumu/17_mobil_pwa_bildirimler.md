# Mobil PWA & Bildirimler Modülü - Geliştirme Durumu

Mobil öncelikli (Mobile-First) erişim stratejisinin temelidir.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Service Worker:** `sw.js` ile çevrimdışı önbellekleme (Stale-While-Revalidate).
- [x] **Manifest.json:** Uygulama ikonu, tema renkleri ve standalone çalışma desteği.
- [x] **Web Push API:** `api/notifications.py` üzerinden bildirim gönderim altyapısı.

## Teknik Altyapı
- **Backend:** `api/notifications.py`.
- **Frontend:** Service Worker JS, Web Push standardı.

## Gelecek Planları
- [ ] **App Store / Play Store Dağıtımı:** TWA (Trusted Web Activity) ile mağazalara entegrasyon.
- [ ] **Coğrafi Bildirimler (Geofencing):** Müşteri bir portföyün yakınından geçerken otomatik bildirim alma.
