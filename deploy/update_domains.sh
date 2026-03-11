#!/usr/bin/env bash
# ==============================================================
# Multi-Domain & SSL Update Script (Enhanced Bootstrapping)
# İmza Gayrimenkul & Mahalle Domains
# ==============================================================

set -euo pipefail

echo "----------------------------------------------------"
echo "  Yeni Alan Adları İçin SSL ve Nginx Güncellemesi"
echo "----------------------------------------------------"

# 1. Nginx ve Klasör Kontrolü
echo "[1/5] Nginx ve bağımlılıklar kontrol ediliyor..."
sudo apt-get update && sudo apt-get install -y nginx certbot python3-certbot-nginx

sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled /var/www/certbot

# 2. GEÇİCİ KONFİGÜRASYON (SSL Olmadan - Sadece Port 80)
# Bu adım Certbot'un doğrulamayı geçebilmesi için gereklidir.
echo "[2/5] Geçici HTTP konfigürasyonu kuruluyor..."
cat <<EOF | sudo tee /etc/nginx/sites-available/imza_temp
server {
    listen 80;
    server_name imzaemlak.com www.imzaemlak.com imzamahalle.com www.imzamahalle.com imzagayrimenkul.com www.imzagayrimenkul.com;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/imza_temp /etc/nginx/sites-enabled/imzagayrimenkul
sudo rm -f /etc/nginx/sites-enabled/default
sudo systemctl restart nginx

# 3. SSL SERTİFİKALARINI AL
echo "[3/5] SSL sertifikaları alınıyor (Certbot)..."
# imzaemlak.com
sudo certbot certonly --webroot -w /var/www/certbot -d imzaemlak.com -d www.imzaemlak.com --non-interactive --agree-tos --email fatihselimkeskin@gmail.com
# imzamahalle.com
sudo certbot certonly --webroot -w /var/www/certbot -d imzamahalle.com -d www.imzamahalle.com --non-interactive --agree-tos --email fatihselimkeskin@gmail.com

# 4. GERÇEK KONFİGÜRASYONA GEÇ (SSL + HTTP2)
echo "[4/5] Gerçek (SSL) Nginx konfigürasyonu uygulanıyor..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
sudo ln -sf /etc/nginx/sites-available/imzagayrimenkul /etc/nginx/sites-enabled/

# Nginx testi ve son restart
sudo nginx -t && sudo systemctl restart nginx

# 5. Temizlik
sudo rm -f /etc/nginx/sites-available/imza_temp

echo "----------------------------------------------------"
echo "  ✅ İşlem Tamamlandı!"
echo "  Portal: https://imzaemlak.com"
echo "  Mahalle: https://imzamahalle.com"
echo "----------------------------------------------------"
