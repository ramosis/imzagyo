# Canlı Sunucu Güncelleme ve Test Rehberi (KESİNLEŞTİ)

Sunucu dizini artık daha profesyonel ve anonim bir yol olan `/opt/imzagyo` olarak güncellenmiştir.

## 🌍 Canlı Altyapı Bilgileri (AI Kopya Kağıdı)
- **SSH Bağlantısı:** `ssh fatihselimkeskin@imza-web-server`
- **Sunucu Dizini:** `/opt/imzagyo`
- **Ana Domain:** `https://imzagayrimenkul.com` (VIP & Yatırım Portalı)
- **Mahalle Portalı:** `https://imzamahalle.com`
- **Backend Portu:** `8000` (Docker Konteynırı)
- **Bağlantı Protokolü:** Nginx SSL (443) -> Proxy Pass (127.0.0.1:8000)

## 🚀 1. Otomatik Güncelleme (TAVSİYE EDİLEN)
Artık sunucuda tek bir komutla tüm süreci (git pull + docker build + restart) yöneten bir script bulunmaktadır:

```bash
# Sunucuya bağlandıktan sonra:
cd /opt/imzagyo
sudo bash deploy/update_app.sh
```

## 🛠️ 2. Manuel Güncelleme Komutları
Eğer yukarıdaki script yerine manuel ilerlemek isterseniz:

```bash
# Doğru dizine git
cd /opt/imzagyo

# Değişiklikleri çek
sudo git pull origin main

# Docker konteynerini tazeleyin
sudo docker-compose down
sudo docker-compose up -d --build

# Nginx ayarlarını tazelemek için (Eğer nginx.conf veya alan adları değiştiyse):
sudo cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
sudo systemctl reload nginx
```

## 🛠️ 3. Çevresel Değişkenler (.env) Onarımı
Eğer `.env` dosyası eksikse veya "Permission Denied" hatası alıyorsanız:

```bash
# Varsa hatalı klasörü sil ve şablonu kopyala
sudo rm -rf .env && sudo cp .env.example .env

# Dosyayı düzenle (Mühürleme)
sudo nano .env
```

> [!IMPORTANT]
> **Kritik Anahtarlar (AI Referans):**
> - `FLASK_APP=wsgi.py` (Faz 28 sonrası giriş noktası)
> - `FLASK_SECRET_KEY` ve `JWT_SECRET` (Eklenti yetkilendirmesi için)

## 👥 Örnek Kullanıcı Bilgileri

| Rol | Kullanıcı Adı | Şifre | Açıklama |
| :--- | :--- | :--- | :--- |
| **Yönetici** | `admin` | `admin123` | Tüm yetkilere sahip ana hesap. |
| **Asistan** | `asistan` | `asistan123` | Portal ve operasyonel araçlar. |
| **Müteahhit** | `muteahhit` | `test1234` | Proje ve mülk sahibi arayüzü. |
| **Kiracı** | `kiraci` | `test1234` | Kiracı paneli ve ödeme takibi. |

## 💡 Hata Giderme Notları
- **GitHub Şifresi:** `git pull` yaptığında şifre isterse, GitHub "Personal Access Token" veya kullanıcı şifreni girmelisin.
- **Log Takibi:** Eğer bir sorun olursa `sudo docker logs imza-backend --tail 50` komutu ile hataları görebilirsiniz.
- **Nginx:** Eğer site hala eski görünüyorsa `sudo systemctl restart nginx` komutunu deneyebilirsin.
