# CRM ve Aday Yönetimi - Hukuki Süreçler

Müşteri verilerinin CRM üzerinde saklanması, KVKK kapsamında en hassas konulardan biridir.

## Veri Saklama ve Onay
- **Açık Rıza:** CRM'e eklenen her müşterinin iletişim izni (SMS, Arama) sistemde dijital bir log olarak saklanır.
- **Erişim Yetkisi:** Danışmanlar sadece kendi bölgelerindeki adaylara erişebilir; bu durum veri güvenliği (Need-to-Know) prensibine uygundur.

## Veri Gizliliği
- Müşteri verileri sunucu taraflı JWT ve bcrypt ile korunmaktadır.
- Veri tabanı yedekleri şifreli (at-rest encryption) şekilde saklanır.