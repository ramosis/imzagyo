# İmza Gayrimenkul — Production Guide

## Proje Yapısı

### Kök Dizin
- `app.py` / `wsgi.py` — Flask entry point'leri (Dev / Prod)
- `requirements.txt` — Python bağımlılıkları
- `frontend/` — Tüm HTML ve Static dosyalar (Modüler yapı)
- `backend/` — Flask uygulaması, core modüller ve paylaşılan servisler

### Altyapı
- `infrastructure/config/` — Docker, .env.example, logrotate
- `infrastructure/nginx/` — Nginx domain yapılandırmaları
- `infrastructure/scripts/` — Deployment ve veritabanı scriptleri

## Hızlı Başlangıç

### Development
```bash
# Bağımlılıkları yükle
pip install -r requirements.txt

# Config ayarla
cp infrastructure/config/.env.example .env
# .env dosyasını kendi anahtarlarınızla düzenleyin

# Başlat
python app.py
```

### Production (Docker)
```bash
docker-compose -f infrastructure/config/docker-compose.prod.yml up -d --build
```

## Test

```bash
# Tüm testleri çalıştır
pytest -v

# Coverage raporu al
pytest --cov=backend --cov-report=html
```

## Deployment

## CI/CD Pipeline

| Ortam | Branch | Trigger | URL |
|-------|--------|---------|-----|
| CI Test | PR / push | Otomatik | GitHub Actions |
| Staging | `develop` | Otomatik | https://staging.imzaemlak.com |
| Production | `main` / tag | Manuel onay | https://imzaemlak.com |

### Deployment Akışı

1. **Staging:** `develop` branch'ine yapılan her push otomatik olarak staging ortamına deploy edilir.
2. **Production:** `main` branch'ine yapılan push'lar veya yeni tag'ler (`v*`) GitHub Actions üzerinden manuel onay bekler. Onay sonrası veritabanı yedeği alınır ve blue-green deployment yapılır.

### Rollback Prosedürü

Herhangi bir hata durumunda (Health Check başarısız olursa), sistem otomatik olarak bir önceki stable commit'e geri döner. Manuel rollback için:

```bash
# SSH ile sunucuya bağlan
ssh user@imzaemlak.com
cd /var/www/imzagyo
git reset --hard <stable-tag-veya-commit>
sudo systemctl restart imzagyo
```

## Geliştirme Kuralları

```bash
# Otomatik deploy scriptini kullan
chmod +x infrastructure/scripts/deploy.sh
./infrastructure/scripts/deploy.sh
```

## Mimarî ve Durum
- **Faz 5 (Production Stabilizasyonu):** TAMAMLANDI.
- **Güvenlik:** CSP, HSTS, Rate Limiting ve CORS aktif.
- **İzleme:** Sentry ve Structured Logging (structlog) aktif.
- **Performans:** Gzip sıkıştırma ve Tarayıcı Cache başlıkları yapılandırıldı.

## Domain'ler
- **imzaemlak.com** — Gayrimenkul & Yatırım
- **imzamahalle.com** — Mahalle & Site Yönetimi
