# 🛠️ Tarayıcı Eklentileri Teknik Geliştirme Planı

Bu plan, Chrome, Opera ve Edge gibi Chromium tabanlı tarayıcılar için ortak bir kod tabanı üzerinden geliştirilecek olan "İmza Emlak Asistanı" eklentisinin uygulama detaylarını içerir.

## 1. Mimari Yaklaşım: Universal Extension
Chrome, Opera ve Edge tarayıcılarının tamamı **Chromium** motorunu kullandığı için **Manifest V3** standardında tek bir kod tabanı (Single Codebase) kullanılacaktır.

- **Framework**: [Plasmo Framework](https://www.plasmo.com/) (React + Tailwind)
  - *Neden?* Otomatik olarak hem Chrome hem Edge için paketleme (build) yapar ve tarayıcı API farklılıklarını minimize eder.
- **Dil**: TypeScript (Hata payını azaltmak için)
- **İletişim**: Flask API (Shadow Bridge) üzerinden gerçek zamanlı veri senkronizasyonu.

---

## 2. Tarayıcı Bazlı Dağıtım Stratejisi

### 🔵 Google Chrome & Opera
- **Mağaza**: Chrome Web Store
- **Yayın**: `manifest.json` dosyası Chrome için optimize edilir. Opera, Chrome eklentilerini doğrudan desteklediği için aynı paket kullanılabilir.
- **Kritik İzinler**: `activeTab`, `storage`, `host_permissions` (İlan siteleri için).

### 🔵 Microsoft Edge
- **Mağaza**: Microsoft Edge Add-ons
- **Farklılıklar**: Edge için özel ikon setleri ve Microsoft Geliştirici hesabı üzerinden doğrulama süreci. Kod tabanı Chrome ile %99 aynı kalacaktır.

---

## 3. Geliştirme Adımları (Teknik Detay)

### 🏗️ Adım 1: Content Script Enjeksiyonu
Her üç tarayıcıda da emlak sitesinin (Sahibinden vb.) DOM yapısına şık bir "İmza Analiz Katmanı" enjekte edilecektir.
- **Z-Index Yönetimi**: Mevcut site tasarımıyla çakışmaması için shadow DOM kullanılacaktır.
- **Data Scraping**: Fiyat, metrekare ve konum verilerini regex ile temizleyip API'ye gönderen asenkron fonksiyonlar.

### 🧠 Adım 2: ROI Hesaplama Motoru (Real-time)
- Eklenti, sayfadaki veriyi okur.
- API'ye (`/api/neighborhood/stats`) konum bilgisini sorar.
- Gelen kira ortalamasıyla "Amortisman Süresi"ni hesaplar ve UI'da gösterir.

### 🥷 Adım 3: Shadow Mode & Arbitraj (Arka Plan)
- Kullanıcı bir ilana baktığında, `background service worker` sessizce bu ilanı ve fiyatı `listings_shadow` tablosuna kaydeder.
- Eğer aynı ilan başka bir sitede daha ucuza bulunursa, eklenti anlık bildirim (Extension Badge veya Toast) ile kullanıcıyı uyarır.

---

## 4. API & Backend Entegrasyonu (Flask)

Eklentinin çalışması için `app.py` tarafında şu uçların (endpoints) stabil olması gerekir:
- `POST /api/tracking/sync`: Eklentiden gelen ilan verilerini kaydeder.
- `GET /api/neighborhood/stats`: Bölge bazlı emsal fiyat verilerini döner.
- `POST /api/leads/extension`: Eklenti üzerinden gelen "Analiz Gör" taleplerini CRM'e yazar.

---

## 5. Güvenlik & Doğrulama
- **Token Tabanlı Erişim**: Eklenti ile Flask API arasındaki iletişim JWT (JSON Web Token) ile güvence altına alınacaktır.
- **Rate Limiting**: Kullanıcıların siteleri gereksiz yere "scrape" etmemesi için Flask-Limiter eklentiden gelen isteklere sınır koyacaktır.

---

> [!TIP]
> **Hizlı Başlangıç**: Plasmo kullanarak `npm run dev` komutuyla her üç tarayıcıda da eşzamanlı testler başlatılabilir.
