# Mahalle Aidat & Finans Modülü - Geliştirme Durumu

Şeffaflık odaklı finansal yönetim modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Borç Takip Sistemi:** Ünite bazlı borçlandırma ve ödeme durumu kaydı.
- [x] **Şeffaf Kasa API:** Yönetim giderlerinin (harcama belgeleriyle beraber) listelenmesi.
- [x] **Tahsilat Raporları:** Danışman paneline düşen genel aidat tahsilat oranı.

## Teknik Altyapı
- **Backend:** `api/neighborhood.py` (Mali modül genişletmesi).
- **Veritabanı:** `apt_dues`, `management_expenses` tabloları.

## Gelecek Planları
- [ ] **Banka Entegrasyonu:** (Sanal POS ile kartla aidat ödeme).
- [ ] **Otomatik Gecikme Zammı:** Geciken aidatlar için kanuni faiz hesaplama botu.