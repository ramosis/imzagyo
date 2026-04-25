# İmza Gayrimenkul

## Proje Yapısı (Aşama 1 Sonrası)

### Kök Dizin (Sadece Gerekli Dosyalar)
- `app.py` / `wsgi.py` — Flask entry point'leri
- `requirements.txt` — Python bağımlılıkları
- `data/` — SQLite veritabanı (runtime)
- `uploads/` — Yüklenen dosyalar (runtime)
- `logs/` — Uygulama logları (runtime)

### Backend
- `app/` — Flask app factory, scheduler (Aşama 2'de backend/app/ olacak)
- `modules/` — İş modülleri (Aşama 2'de backend/core/ + addons/ olacak)
- `shared/` — Ortak servisler, modeller (Aşama 2'de backend/shared/ olacak)

### Frontend
- `pages/` — HTML sayfaları (Aşama 2'de frontend/ altına taşınacak)
- `static/` — CSS, JS, images (Aşama 2'de frontend/ altına taşınacak)

### Mobil & Eklentiler
- `mobile/` — React Native / Expo app
- `extension/` / `extension-pro/` — Tarayıcı eklentileri

### Altyapı
- `infrastructure/` — Docker, scriptler, dokümanlar, nginx config
- `tests/` — Testler
- `archived/` — Legacy kodlar

## Başlatma

```bash
# Geliştirme
python app.py

# Docker
docker-compose -f infrastructure/config/docker-compose.yml up
```

## Domain'ler
- **imzaemlak.com** — Gayrimenkul & Yatırım
- **imzamahalle.com** — Mahalle & Site Yönetimi
