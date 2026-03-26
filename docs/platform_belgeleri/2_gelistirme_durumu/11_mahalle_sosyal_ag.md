# Mahalle Sosyal Ağ Modülü - Geliştirme Durumu

Topluluk aidiyetini artıran iletişim modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Duyuru Sistemi:** Admin paneli ve mahalle portalı arasında senkron duyuru yayını.
- [x] **Basit Mesajlaşma:** WebSockets (Socket.io) altyapısının temelleri atıldı.
- [x] **Profil Doğrulama:** Sadece `apt_residents` tablosunda kaydı olanların mesajlaşabilmesi.

## Teknik Altyapı
- **Backend:** `api/neighborhood.py` (Sosyal genişletme).
- **Gerçek Zamanlı İletişim:** Socket.io (Opsiyonel) veya Long Polling.

## Gelecek Planları
- [ ] **Eşya Paylaşım Marketi:** (Komşular arası ikinci el eşya takası/satışı).
- [ ] **Etkinlik Yönetimi:** (Sitede barbekü partisi, yoga etkinliği düzenleme).