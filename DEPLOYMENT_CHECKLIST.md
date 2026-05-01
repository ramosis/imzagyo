# 🚀 IMZA GYO - DEPLOYMENT CHECKLIST (%100 Complete)

Bu liste, İmza Gayrimenkul platformunun canlı ortama (Production) güvenli bir şekilde alınması için gereken adımları içerir.

## 1. 🛠️ Ortam Hazırlığı (Environment)
- [ ] `.env` dosyasının production değerleri ile oluşturulduğundan emin olun.
- [ ] `FLASK_ENV=production` olarak ayarlandı.
- [ ] `SECRET_KEY` ve `SECURITY_PASSWORD_SALT` güçlü random değerlerle değiştirildi.
- [ ] Veritabanı (PostgreSQL) erişim bilgileri doğrulandı.

## 2. 🗄️ Veritabanı (Database & Migrations)
- [ ] PostgreSQL servisi çalışıyor.
- [ ] `python -m alembic upgrade head` komutu ile tüm tablolar oluşturuldu.
- [ ] Gerekli "Seed" verileri (roles, default admin) yüklendi.

## 3. 🌐 Network & Security
- [ ] Nginx konfigürasyonu (`infrastructure/nginx/`) aktif edildi.
- [ ] SSL sertifikaları (Certbot/Let's Encrypt) yüklendi.
- [ ] Güvenlik duvarında (UFW/Security Group) sadece 80, 443 ve monitoring portları açık.
- [ ] CORS ayarlarında sadece izin verilen domainler (`imzaemlak.com`) var.

## 4. 📦 Docker & Containers
- [ ] `docker-compose -f infrastructure/config/docker-compose.yml up -d` komutu çalıştırıldı.
- [ ] Tüm container'ların (`app`, `db`, `prometheus`, `grafana`) "Up" olduğu doğrulandı.
- [ ] Image'lar en son `main` branch'inden build edildi.

## 5. 🔍 Monitoring & Logging
- [ ] Sentry DSN doğru şekilde set edildi ve test edildi.
- [ ] Prometheus metrikleri (`/metrics`) dışarıya veri sızdırmayacak şekilde korundu.
- [ ] Grafana dashboard'ları yüklendi ve AlertManager Slack webhook'u test edildi.

## 6. 📂 Assets & Frontend
- [ ] Statik dosyalar (`frontend/static/`) Nginx tarafından sunuluyor.
- [ ] Lazy-load modülleri (`customer_portal.js`, `crm.js` vb.) tarayıcıda hatasız yükleniyor.
- [ ] Logo ve font yolları (absolute path) kontrol edildi.

## 7. 🤖 Integrations
- [ ] Google OAuth Client ID ve Secret set edildi.
- [ ] Gemini API Key doğrulandı.
- [ ] Cloudinary / S3 saklama alanları erişilebilir durumda.

## 8. 🧪 Son Testler (Smoke Test)
- [ ] Ana sayfa yükleniyor.
- [ ] Admin login yapılabiliyor.
- [ ] Müşteri portalı timeline verilerini çekiyor.

## 9. 🚀 Go-Live
- [ ] DNS kayıtları (A record) yeni sunucuya yönlendirildi.
- [ ] Health Check (`/health`) endpoint'i izlemeye alındı.

## 10. 🧹 Post-Deployment
- [ ] Geçici "cleanup" scriptleri silindi.
- [ ] `.git` klasörü production'da sadece gerekli yetkilere sahip.

---
**Durum:** Hazır! 🥂
