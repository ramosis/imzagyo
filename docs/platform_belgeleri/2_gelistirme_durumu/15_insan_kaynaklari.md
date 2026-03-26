# İnsan Kaynakları Modülü - Geliştirme Durumu

Ekip verimliliği ve organizasyonel yapı modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Ekip Yönetim API:** `api/hr.py` ile personel ekleme/silme/güncelleme.
- [x] **Puantaj ve KPI Dashboard:** Saha verileriyle entegre çalışan performans ekranı.
- [x] **Danışman Uzmanlık Tanımları:** Hangi mahallede kimin yetkili olduğunu (`ekip` tablosu) yönetme.

## Teknik Altyapı
- **Backend:** `api/hr.py` ve `api/users.py`.
- **Veritabanı:** `hr_performance`, `hr_documents` tabloları.

## Gelecek Planları
- [ ] **Otomatik Prim Hesaplama:** Satış sözleşmelerine göre hakedişi hesaplayan algoritma.
- [ ] **Eğitim Platformu (LMS):** Yeni danışmanlar için video eğitim ve sınav modülü.