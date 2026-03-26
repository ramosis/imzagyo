# MLS Modülü - Geliştirme Durumu

Emlak iş ağını otomatize eden "Birlikte Kazan" modülüdür.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Daire Başlıklı Yetkilendirme:** `inner` ve `outer` daireler için farklı veri görünürlüğü.
- [x] **Eşleştirme Motoru:** Lokasyon, Kategori ve Bütçe bazlı otomatik eşleştirme algoritması.
- [x] **MLS Marketplace UI:** `mls.html` üzerinden havuzdaki ilanların ve taleplerin izlenmesi.

## Teknik Altyapı
- **Backend:** `api/mls.py` Blueprint.
- **Veritabanı:** `mls_listings`, `mls_demands`, `mls_trust_scores` tabloları.

## Gelecek Planları
- [ ] **Global MLS Entegrasyonu:** (RE-OS veya ListGlobally API ile portföy takası).
- [ ] **Blockchain Tabanlı Komisyon Escrow:** Komisyon paylaşımının akıllı sözleşmelerle güvenceye alınması.
