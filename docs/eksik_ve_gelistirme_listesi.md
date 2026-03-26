# İmza GYO: Kapsamlı Eksik ve Geliştirme Listesi 🚀

Bu döküman, projenin mevcut durumundaki teknik borçları, güvenlik açıklarını, eksik fonksiyonları ve gelecekteki büyüme potansiyelini (Global Vizyon) içeren detaylı bir listedir.

---

## 1. Teknik Altyapı & Güvenlik (Kritik) 🛡️
- [ ] **Güçlü Şifreleme:** Şu an kullanılan `SHA256` yerine `bcrypt` veya `argon2` gibi tuzlanmış (salted) algoritmaya geçiş.
- [ ] **JWT Güvenliği:** Secret key'in sadece `.env`'den okunması ve token süresi dolduğunda "Refresh Token" mekanizması.
- [ ] **Giriş Doğrulama (Validation):** Tüm API uç noktalarında Marshmallow şemalarının eksiksiz uygulanması (Parties, Contracts, Tasks vb. için eksik).
- [ ] **Hata Yönetimi (Logging):** Yeni eklenen Sentry ve Logging yapısının tüm `api/` modüllerine yayılması (try-except bloklarında `logger.error` kullanımı).
- [ ] **Veritabanı İndeksleme:** Sık sorgulanan alanlara (Örn: `tc_no`, `refNo`, `lead_id`) veritabanı indeksleri eklenerek performans artışı sağlanması.
- [ ] **API Dokümantasyonu:** Swagger/OpenAPI entegrasyonu ile teknik dökümantasyonun otomatikleştirilmesi.

## 2. Eksik Fonksiyonlar (Ürün Gelişimi) 🛠️
- [ ] **Birleşik İşlem Zaman Çizelgesi (Unified Timeline):** Mevcut parça parça timeline'ların (LMetrics Dijital İz, Saha Takip Rotaları, Pipeline Geçmişi) tek bir "Müşteri Yolculuğu" ekranında birleştirilmesi.
- [ ] **Müşteri Takip Paneli (Compass Modeli):** Müşterilerin tapu, ekspertiz ve sözleşme sürecini canlı izleyebileceği şeffaf dış arayüz.
- [ ] **Gelişmiş Filtreleme:** Web sitesinde mülk tipi, fiyat aralığı ve özellik bazlı detaylı arama motoru.
- [ ] **Medya Optimizasyonu:** Sunucuya yüklenen görsellerin otomatik WebP formatına dönüştürülmesi ve boyutlandırılması.
- [ ] **Bildirim Merkezi:** Sadece in-app değil, kritik durumlarda (Sözleşme onayı vb.) SMS veya E-Posta ile push notification.
- [ ] **Sosyal Medya Girişi (OAuth2):** Kullanıcıların Google, Facebook veya Instagram hesaplarıyla hızlı ve güvenli bir şekilde giriş yapabilmesi.
- [ ] **Mobil Uygulama (Müşteri):** Müşterilerin ilan bakabileceği ve süreçlerini takip edebileceği native/cross-platform uygulama.

## 3. Global Vizyon & AI Adaptasyonu (Yıldız Haritası) 🌟
- [ ] **Güneş Işığı Simülasyonu (Beike Modeli):** Mülkün cephesine göre günün hangi saatinde ne kadar ışık alacağının teknik analizi.
- [ ] **AI Chatbot (Türkçe NLP):** Müşteri sorularını doğal dilde yanıtlayan ve L-Metrics puanlamasına veri sağlayan asistan.
- [ ] **Akıllı Kilit Entegrasyonu (Zigbang Modeli):** Danışmanlar için geçici dijital anahtar ve "Self-Showing" (Kendi kendine evi gezme) altyapısı.
- [ ] **Semt Karnesi:** Tapu verileri ve sosyal donatıları (okul, eczane, market) birleştirerek semt bazlı yatırım puanı üretme.

## 4. Kullanıcı Deneyimi (UX) & Performans 💎
- [ ] **Modern State Management:** Frontend tarafında (jQuery yerine) Vue.js veya React gibi bir yapıya geçerek daha hızlı/interaktif arayüzler.
- [ ] **Global Dashboard:** Adminler için tüm saha operasyonunu, kampanya verimini ve finansal durumu tek ekranda özetleyen "Executive Dashboard".
- [ ] **Karanlık Mod (Dark Mode):** Tüm portal ve web sitesi için premium karanlık tema desteği.
- [ ] **PWA Desteği:** Web sitesinin mobil cihazlarda bir uygulama gibi ana ekrana eklenmesi ve offline çalışabilme yeteneği.

---

## 📅 Önceliklendirme (Priority Matrix)

| Görev | Etki | Zorluk | Öncelik |
|-------|------|--------|---------|
| Şifreleme & Güvenlik | Yüksek | Düşük | 🔴 KRİTİK |
| Müşteri Takip Timeline | Yüksek | Orta | 🔴 YÜKSEK |
| API Doğrulamaları (Schemas) | Orta | Düşük | 🟡 ORTA |
| Güneş Işığı Analizi | Orta | Yüksek | 🔵 VİZYON |
| Mobil Uygulama | Yüksek | Çok Yüksek | 🔵 VİZYON |
