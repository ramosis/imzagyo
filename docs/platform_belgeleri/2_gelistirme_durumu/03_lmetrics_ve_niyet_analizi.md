# LMetrics ve Niyet Analizi Modülü - Geliştirme Durumu

Bu modül, platformun en özgün teknolojik altyapılarından biridir.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Davranış Takip Kütüphanesi:** `js/analytics/lmetrics.js` ile scroll, click ve active-time takibi.
- [x] **Niyet Skoru Algoritması:** Backend'de toplanan verilerin ağırlıklandırılarak 0-100 arası skorlanması.
- [x] **Veri Toplama:** `user_behavior` tablosu üzerinden büyük veri (Big Data) toplama altyapısı.

## Teknik Altyapı
- **Frontend:** Intersection Observer API ile görünürlük (visibility) takibi.
- **Backend:** `api/analytics.py` - Verilerin asenkron olarak kaydedilmesi.
- **Veritabanı:** `site_analytics`, `intent_scores` tabloları.

## Gelecek Planları
- [ ] **Prediktif Analiz:** Gelecek ay hangi bölgelerin parlayacağını tahmin eden AI modeli.
- [ ] **Kişiselleştirilmiş Öneriler:** Davranış verisine göre ana sayfada mülk önerme.