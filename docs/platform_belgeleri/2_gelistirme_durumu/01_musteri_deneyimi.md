# Müşteri Deneyimi Modülü - Geliştirme Durumu

Mevcut modül, kurumsal web sitesinin ( `anasayfa.html`, `detay.html` vb.) tüm bileşenlerini ve bunların veri tabanı ile olan bağlantısını kapsar.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Responsive Tasarım:** Tüm sayfalarda mobil öncelikli (Mobile-First) yaklaşım uygulandı.
- [x] **Dinamik Portföy Listeleme:** `database.py` üzerindeki `portfoyler` tablosundan anlık veri çekimi.
- [x] **I18n Altyapısı:** `js/i18n.js` ile tüm ana site metinlerinin dile göre değişimi sağlandı.

## Teknik Altyapı
- **Frontend:** Vanilla JS, CSS3 (Glassmorphism), HTML5.
- **Backend:** Python Flask API (`app.py`).
- **Veritabanı:** SQLite3 - `site_settings` ve `pages` tabloları.

## Gelecek Planları
- [ ] **A/B Test Altyapısı:** Ziyaretçilerin en çok hangi Hero başlığına tıkladığını ölçen sistem.
- [ ] **Hız Optimizasyonu:** WebP sonrası, JavaScript dosyalarının bundle edilerek küçültülmesi.