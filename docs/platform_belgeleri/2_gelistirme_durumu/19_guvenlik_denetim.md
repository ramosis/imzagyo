# Güvenlik & Denetim Modülü - Geliştirme Durumu

Sistem bütünlüğünü ve veri mahremiyetini sağlayan koruma katmanıdır.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Rate Limiter:** `flask_limiter` ile kaba kuvvet (Brute Force) saldırı koruması.
- [x] **Sentry Entegrasyonu:** Gerçek zamanlı hata ve güvenlik zafiyeti takibi.
- [x] **Şifreleme (Bcrypt):** Tüm şifrelerin güvenli hash algoritmasıyla saklanması.
- [x] **RBAC (Yetki Kontrolü):** 'yonetici', 'danisman', 'sakin' rolleri bazlı erişim kısıtlaması.

## Teknik Altyapı
- **Backend:** `app.py` (Middlewares), Flask-Limiter.
- **Logging:** Python Logging Module & Sentry.

## Gelecek Planları
- [ ] **WAF (Web Application Firewall):** SQL injection ve XSS saldırılarına karşı proaktif koruma duvarı.
- [ ] **Hizmet Kesinti İzleme (Uptime):** 7/24 erişilebilirlik takibi.
