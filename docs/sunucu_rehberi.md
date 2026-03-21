# Canlı Sunucu Güncelleme ve Test Rehberi (KESİNLEŞTİ)

Sunucu dizini artık daha profesyonel ve anonim bir yol olan `/opt/imzagyo` olarak güncellenmiştir.

## 🚀 1. Sunucu Güncelleme Komutları
Sunucuya SSH ile bağlandıktan sonra şu komutları sırasıyla çalıştırın:

```bash
# Klasörünüz hala eski yerindeyse bir defaya mahsus taşıyın:
# sudo mv ~/imzagyo /opt/imzagyo
# sudo chown -R www-data:www-data /opt/imzagyo

# Doğru dizine git
cd /opt/imzagyo

# Değişiklikleri çek
sudo git pull origin main

# Docker konteynerini tazeleyin (Konteyner ismi: imza-backend)
sudo docker-compose down
sudo docker-compose up -d --build

# Nginx ayarlarını tazelemek için (Eğer nginx.conf değiştiyse):
sudo cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
sudo systemctl reload nginx
```

## 👥 Örnek Kullanıcı Bilgileri

| Rol | Kullanıcı Adı | Şifre | Açıklama |
| :--- | :--- | :--- | :--- |
| **Yönetici** | `admin` | `admin123` | Tüm yetkilere sahip ana hesap. |
| **Asistan** | `asistan` | `asistan123` | Portal ve operasyonel araçlar. |
| **Müteahhit** | `muteahhit` | `test1234` | Proje ve mülk sahibi arayüzü. |
| **Kiracı** | `kiraci` | `test1234` | Kiracı paneli ve ödeme takibi. |

## 🛠️ Hata Giderme Notları
- **GitHub Şifresi:** `git pull` yaptığında şifre isterse, GitHub "Personal Access Token" veya kullanıcı şifreni girmelisin.
- **Nginx:** Eğer site hala eski görünüyorsa `sudo systemctl restart nginx` komutunu deneyebilirsin.
