🚀 Emlak Yatırım Danışmanı (Tarayıcı Eklentisi) - Master Plan

Bu doküman, ilan sitelerinde (Sahibinden, Hepsiemlak vb.) gezinirken kullanıcılara anlık ROI (Amortisman) analizi sunan, arka planda potansiyel müşteri (lead) toplayan ve ilan arbitrajı (fiyat farkı) yakalayan tarayıcı eklentisinin geliştirme yol haritasıdır.

🏗️ FAZ 1: MVP (Minimum Çalışan Ürün) - Temel Değer ve Lead Toplama

Hedef: En hızlı şekilde pazara çıkmak, ROI analizini göstermek ve yatırımcılardan iletişim bilgisi (lead) toplamaya başlamak.
Süre Tahmini: 3-4 Hafta

1.1. Eklenti Ön Yüzü (Chrome Extension - Manifest V3)

İskelet Kurulumu: manifest.json dosyasının oluşturulması. Sadece belirli emlak sitelerinde (beyaz liste) çalışma izninin (permissions) ayarlanması.

Veri Okuyucu (Content Script): Sahibinden ve Hepsiemlak ilan sayfalarından Fiyat, Brüt/Net m², Oda Sayısı, Kat, İl/İlçe/Mahalle verilerini okuyacak DOM (HTML) seçicilerin yazılması.

UI Enjeksiyonu (Tasarım): İlan fotoğraflarının hemen yanına veya fiyatın altına şık bir "Yatırım Analiz Kutusu" yerleştirilmesi.

Açık Veri: "Bölge Amortisman Ortalaması: 18 Yıl"

Bulanık (Gizli) Veri: "Bu İlana Özel ROI Skoru: %X"

Lead Formu (Kanca): Gizli veriyi açmak için "Ücretsiz Gör/Kayıt Ol" butonu ve Google/Telefon numarası ile hızlı üyelik akışı.

1.2. Backend ve Veritabanı (API & DB)

Sunucu Kurulumu: Node.js/Python tabanlı, eklentiden gelen istekleri saniyeler içinde yanıtlayacak hızlı bir REST API.

Temel Veritabanı Şeması (PostgreSQL / MongoDB):

users: Kullanıcı bilgileri (Ad, Tel, İlgilendiği Bölgeler).

region_stats: Pilot bölgelerin (örn. Kadıköy, Ataşehir) ortalama m² satış ve kira fiyatları (Manuel veya şirket içi veriyle beslenecek).

listings_shadow: (Gölge Modu için) Kullanıcıların gezdiği ilanların arka planda kaydedileceği tablo.

ROI Algoritması: Eklentiden gelen ilan fiyatını, veritabanındaki bölge kira ortalamasına bölüp amortisman süresini hesaplayan fonksiyon.

🧠 FAZ 2: Hibrit Çalışma Modeli (Kitle Kaynaklı Öğrenme)

Hedef: Eklentinin dünyadaki tüm web sitelerinde (yerel emlakçılar, yurtdışı siteleri) kullanıcı yardımıyla çalışabilir hale gelmesi.
Süre Tahmini: 2-3 Hafta

2.1. "Track" (Analiz Et) Modülü

Manuel Tetikleme: Beyaz listede olmayan bir sitede, kullanıcının eklenti ikonuna tıklayıp "Bu sayfayı analiz et" demesi.

Öğretici (Onboarding) UI: Ekranı hafifçe karartıp kullanıcıdan sırasıyla şunları seçmesini isteyen araç çubuğu:

"Fiyata tıkla"

"Oda sayısına tıkla"

"Metrekareye tıkla"

Site Haritalama Algoritması: Kullanıcının tıkladığı HTML elementlerinin XPath/CSS Selector yollarını alıp arka plandaki site_maps tablomuza (domain bazlı) kaydetmek.

Otomatik Devreye Girme: Aynı siteye giren ikinci kullanıcıda, eklentinin veritabanına sorup "Ben bu siteyi biliyorum" diyerek otomatik çalışmaya başlaması.

🥷 FAZ 3: Shadow Mode (Gölge Modu) & İlan Arbitrajı

Hedef: Piyasada aynı evin farklı fiyatlarla satıldığı durumları yakalayıp, kullanıcıya "Aynı ev X sitesinde daha ucuz!" bildirimi sunmak.
Süre Tahmini: 3-4 Hafta

3.1. Arka Plan Veri Toplama (Shadow Mode)

Eklentinin okuduğu her ilanı listings_shadow tablosuna sessizce kaydetmesi.

Stale Data (Çöp Veri) Yönetimi: Tablodaki her ilana last_seen_at (son görülme) tarihi eklenmesi. 15 gün güncellenmeyen ilanların statüsünün is_active=false yapılması.

3.2. Fuzzy Matching (Bulanık Eşleştirme) Motoru

Sunucuda her gece (veya anlık) çalışan bir algoritma:

Kural 1: Mahalle AYNI MI?

Kural 2: Oda Sayısı AYNI MI?

Kural 3: Metrekare farkı %10'dan AZ MI?

Kural 4: Kat bilgisi BENZER Mİ?

Bildirim Sistemi (Bölgesel Lansman): Algoritma yeterince veri topladıktan sonra, pilot bölgelerde eşleşen ilanlar için eklenti arayüzünde "🚨 Fiyat Alarmı: Bu ev başka bir sitede %10 daha ucuz" UI'ının aktif edilmesi.

🤝 FAZ 4: Pazaryeri (Matchmaking) & Global Ölçekleme

Hedef: Kiracılar ile yatırımcıları birleştirmek ve yurtdışı pazarı için altyapıyı hazırlamak.

4.1. Kiracı - Yatırımcı Eşleşmesi

Kiracılar için özel "Emsal Kira" ve "Gerçek Gider (Aidat vb.)" analiz kutularının tasarlanması.

"Bana uygun ev çıkınca haber ver" bekleme listesi (Waitlist) formunun eklenmesi.

Satış ekibi CRM'ine, yatırımlık ilana bakan kullanıcı ile o bölgede ev arayan kiracıyı eşleştiren uyarı sisteminin entegrasyonu.

4.2. Global SaaS Hazırlığı (Opsiyonel)

Eklentinin White-Label (Kiralık Yazılım) olarak İngilizce dil desteğiyle paketlenmesi.

Stripe ödeme altyapısı entegrasyonu (Yurtdışı son kullanıcıları için aylık 9.99$ premium veri aboneliği).

🛠️ Tavsiye Edilen Teknoloji Yığını (Tech Stack)

Eklenti Frontend: React.js, Tailwind CSS (Hızlı ve şık UI için), Plasmo Framework (Chrome eklentisi geliştirmeyi inanılmaz hızlandırır).

Backend: Node.js (Express/NestJS) veya Python (FastAPI - Veri analizi ve eşleştirme için daha uygundur).

Veritabanı: PostgreSQL (İlişkisel veriler için). Arama ve eşleştirme operasyonları hızlandığında ElasticSearch eklenebilir.