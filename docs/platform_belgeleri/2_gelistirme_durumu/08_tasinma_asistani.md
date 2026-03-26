# Taşınma Asistanı Modülü - Geliştirme Durumu

Müşteri memnuniyetini en üst düzeye çıkaran operasyonel bir modüldür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Dinamik Kontrol Listesi:** SQL üzerinde tutulan ve kullanıcı bazlı ilerleme durumunu kaydeden altyapı.
- [x] **Hizmet Sağlayıcı Entegrasyonu:** `neighborhood_facilities` tablosuna nakliye ve depo firmalarının (icon destekli) eklenmesi.

## Teknik Altyapı
- **Backend:** `api/neighborhood.py` (Genişletildi).
- **Veritabanı:** `relocation_checklist` ve `service_providers` tabloları.

## Gelecek Planları
- [ ] **Abonelik Taşıma Botu:** Kamu kuruluşlarının (E-devlet üzerinden) aboneliklerini tek tıkla taşıma entegrasyonu.
- [ ] **Eşya Sigorta Teklifi:** Anlık taşınma sigortası poliçesi başlatma özelliği.