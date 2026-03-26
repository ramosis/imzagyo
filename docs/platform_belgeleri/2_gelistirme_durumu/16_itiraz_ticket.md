# İtiraz & Ticket Modülü - Geliştirme Durumu

Süreç iyileştirme ve geribildirim modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Ticket API:** Taleplerin veritabanına kaydı ve durum yönetimi.
- [x] **E-Posta Bildirimi:** Yeni talep geldiğinde ilgili danışmana otomatik uyarı.

## Teknik Altyapı
- **Backend:** `api/support.py` (Genel destek modülü).
- **Veritabanı:** `tickets`, `ticket_replies` tabloları.

## Gelecek Planları
- [ ] **AI Sentiment Analysis:** Gelen şikayetlerin aciliyetini ve tonunu (kızgın, üzgün vb.) ölçen yapay zeka.
- [ ] **SLA Takibi:** Taleplerin belirli bir sürede çözülmemesi durumunda üst yönetime otomatik "Escalation".
