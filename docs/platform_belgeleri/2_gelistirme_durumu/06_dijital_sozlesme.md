# Dijital Sözleşme Modülü - Geliştirme Durumu

Süreç otomasyonunun kritik bir ayağıdır.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Şablon Yönetimi:** `api/contract_templates.py` ile dinamik şablon desteği.
- [x] **PDF Oluşturma:** Taslakların PDF formatında döküm alınabilmesi.
- [x] **Sözleşme Takibi:** `contracts` tablosu üzerinden tarihçe ve durum (taslak, imzalandı, iptal) yönetimi.

## Teknik Altyapı
- **Backend:** Flask Blueprint (`contracts_bp`).
- **Veritabanı:** `contracts`, `contract_templates` tabloları.

## Gelecek Planları
- [ ] **E-İmza Entegrasyonu:** (BTK onaylı servis sağlayıcılar üzerinden).
- [ ] **Blokzincir Onayı:** Sözleşme özetinin (hash) blokzincirine kaydedilerek değiştirilemezliğinin sağlanması.