# Mobil Uygulama Geliştirme Notları: İmza Super App

Bu doküman, "İmza Gayrimenkul" markası için geliştirilmesi planlanan mobil uygulama ekosisteminin konseptini, modüllerini ve teknik yol haritasını özetlemektedir.

## 1. Genel Konsept: "İkili Uygulama Ekosistemi"

Farklı kullanıcı kitlelerinin (VIP yatırımcılar vs. mahalle sakinleri) farklı beklentileri ve güvenlik gereksinimleri olduğundan, sistem **iki ayrı mobil uygulama** olarak kurgulanacaktır. Ancak her iki uygulama da **aynı merkezi veritabanı ve backend API'sine (Flask)** bağlanacaktır.

### Uygulama 1: İmza Gayrimenkul & Yatırım (Core / VIP App)
- **Hedef Kitle:** Mülk Sahipleri, VIP Yatırımcılar, Alıcılar.
- **Odak:** Ciddi finansal işlemler, ROI takibi, sözleşmeler, portföy arama ve gayrimenkul operasyonları.
- **Tasarım Dili:** Son derece lüks, premium (siyah/altın detaylar), veri odaklı ve profesyonel.

### Uygulama 2: İmza Mahalle (Topluluk / Hizmet App)
- **Hedef Kitle:** Kiracılar, Site/Mahalle Sakinleri.
- **Odak:** Gündelik yaşamı kolaylaştırma, arıza talepleri (concierge), aidat ödemeleri, esnaf ağı ve tartışmasız (no-conflict) yardımlaşma panosu.
- **Tasarım Dili:** Daha samimi, erişilebilir, fonksiyonel ve hızlı etkileşim odaklı.

-   **Merkezi Kimlik Doğrulama:** Mevcut `api/auth.py` endpoint'i, uygulamalar için JWT (JSON Web Token) tabanlı kimlik doğrulama mekanizması ile genişletilmelidir. Sistem, kullanıcının rolüne göre hangi uygulamaya girebileceğini veya neler görebileceğini yönetir.

---

## 2. Uygulama Modülleri

### Uygulama 1 Kapsamı (İmza Gayrimenkul & Yatırım)

#### Modül A: İmza Yatırım (Mülk Sahibi ve Yatırımcı Paneli)

-   **API Entegrasyonları:**
    -   `GET /api/contracts`: Kiracının kendi sözleşme detaylarını görmesi için.
    -   `POST /api/maintenance`: Arıza ve bakım talebi oluşturmak için. (Fotoğraf yükleme özelliği eklenmeli).
    -   `GET /api/taxes`: Aidat ve diğer borçları görüntülemek için.
    -   `POST /api/finance/pay`: Online ödeme entegrasyonu için (kredi kartı vb.).
-   **Özellikler:**
    -   **Dijital Concierge:** "Musluk damlatıyor" gibi taleplerin fotoğraf/video ile kolayca oluşturulması.
    -   **Finansal İşlemler:** Kira ve aidatların uygulama üzerinden ödenmesi, geçmiş ödemelerin görüntülenmesi.
    -   **Duyurular:** Site yönetiminden gelen duyuruların anlık bildirim (push notification) ile alınması.
    -   **Misafir Yönetimi:** Güvenlik için misafirlere süreli QR kod ile giriş izni oluşturma.

    -   **Kurumsal İletişim:** Gayrimenkul danışmanları ile doğrudan ve güvenli iletişim kanalı.

### Uygulama 2 Kapsamı (İmza Mahalle)

#### Modül B: İmza Yaşam (Kiracı ve Mülk Sakini Özellikleri)

Bu modül, kiracıların ve sitede oturanların site/mahalle yönetimini ilgilendiren operasyonlarını kapsar.

-   **API Entegrasyonları:**
    -   `GET /api/portfoyler`: Mülk sahibinin kendi mülklerini listelemesi için.
    -   `GET /api/contracts`: Mülke bağlı sözleşmeleri (kiracı bilgilerini) görmesi için.
    -   `GET /api/expenses`: Mülk için yapılan harcamaları (fatura görselleriyle) takip etmesi için.
    -   `GET /api/finance`: Kira gelirlerinin yatıp yatmadığını anlık olarak görmesi için.
-   **Özellikler:**
    -   **Varlık Yönetim Paneli:** Portföyün toplam değeri, aylık/yıllık kira getirisi (ROI) gibi metriklerin grafiklerle sunulması.
    -   **Şeffaf Finans:** Yapılan tüm masrafların (vergi, bakım, onarım) ve elde edilen gelirlerin detaylı dökümü.
    -   **Raporlama:** Aylık veya yıllık gelir-gider raporlarının PDF olarak indirilebilmesi.

    -   **Misafir Yönetimi:** Güvenlik için misafirlere süreli QR kod ile giriş izni oluşturma.

#### Modül C: İmza İş Birliği (Fayda ve Hizmet Odaklı Pano)

Bu modül, bir "Sosyal Medya" değildir. Tartışma, yorum veya beğeni özellikleri kapalıdır. Amaç sadece mahalle/site sakinlerinin hayatını kolaylaştıracak iş birlikleri ve duyurulardır.

-   **API Entegrasyonları:**
    -   `GET /api/neighborhood/businesses`: Bölgedeki "İmza Onaylı" esnafları listelemek için. Kategoriye göre filtreleme (`?category=Restoran`).
    -   `GET /api/campaigns`: Esnafların veya İmza Gayrimenkul'ün sunduğu özel kampanyaları ve indirimleri göstermek için.
    -   `GET /api/neighborhood/posts`: İş birliği panosunu çekmek için.
    -   `POST /api/neighborhood/posts`: Yeni bir ilan veya duyuru paylaşmak için.
-   **Özellikler:**
    -   **Onaylı Esnaf Ağı:** İmza Gayrimenkul referanslı güvenilir işletmeler.
    -   **İş Birliği Panosu (No-Conflict Zone):**
        -   **Ulaşım/Servis:** "Her sabah 08:00'de 2. Sanayi'ye servis kalkacaktır" (Yönetim) veya "Maslak yönüne giden var mı?" (Sakin).
        -   **Paylaşım:** "Çocuğumun küçülen bisikletini veriyorum."
        -   **Duyuru:** Yönetimden gelen su kesintisi, ilaçlama vb. resmi bilgiler.
    -   **Kurallar:** Gönderilere yorum yapılamaz, sadece "İletişime Geç" butonu ile doğrudan mesaj/arama yapılabilir. Bu sayede polemik ve çatışma engellenir.

---

## 3. Teknik Notlar ve Yol Haritası

-   **Mobil Teknoloji:** Geliştirme hızı ve maliyet etkinliği açısından **React Native** veya **Flutter** gibi cross-platform (iOS & Android) bir teknoloji tercih edilmelidir.
-   **Backend (API):** Mevcut Flask altyapısı, mobil uygulama için bir REST API görevi görecektir. Tüm veri alışverişi JSON formatında olacaktır.
-   **Anlık Bildirimler (Push Notifications):** Firebase Cloud Messaging (FCM) veya OneSignal gibi bir servis kullanılarak "Yeni duyuru var", "Kiranız yattı", "Bakım talebiniz tamamlandı" gibi anlık bildirimler gönderilmelidir.
-   **Harita ve Konum Servisleri:** "İmza Mahalle" modülündeki esnafların konumlarını göstermek için Google Maps veya Mapbox entegrasyonu gereklidir.
-   **Fazlandırma (MVP - Minimum Uygulanabilir Ürün):**
    1.  **Faz 1 (Core API & Yatırım App MVP):** Backend JWT doğrulamasının yazılması. "İmza Gayrimenkul & Yatırım" uygulamasının temel portföy listeleme ve sözleşme özellikleri.
    2.  **Faz 2 (İmza Mahalle MVP):** "İmza Mahalle" uygulamasının ayağa kaldırılması, esnaf listeleme ve arıza/bakım talebi oluşturma.
    3.  **Faz 3 (Sosyal & Finans):** İş birliği panosu (Mahalle) ve detaylı finansal ROI grafikleri (Yatırım).