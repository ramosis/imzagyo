# İmza Gayrimenkul Platform v2

Modern, modüler ve lüks gayrimenkul yönetim platformu.

## 📁 Proje Yapısı

- **🟦 backend/**: Flask çekirdek uygulama ve Blueprint tabanlı modüller (Core/Addons).
- **🟨 frontend/**: Çoklu alan adı destekli frontend yapısı (Investment, Neighborhood, Portal).
- **🟪 infrastructure/**: Konfigürasyon, dokümantasyon ve yardımcı scriptler.
- **🟩 mobile/**: React Native / Expo mobil uygulama.
- **💾 data/ & uploads/**: Veritabanı ve medya dosyaları.

## 🚀 Hızlı Başlatma

```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Uygulamayı başlat
python app.py
```

## 🛠️ Mimari Prensipler

- **İzolasyon**: Her modül kendi Blueprint'i ile izole edilmiştir.
- **Genişletilebilirlik**: Yeni özellikler `addons` klasörüne eklenerek dinamik olarak yüklenebilir.
- **Hibrit Frontend**: Aynı backend üzerinden `imzaemlak.com` ve `imzamahalle.com` domainleri yönetilir.

---
*İmza Gayrimenkul Geliştirme Ekibi*
