#!/usr/bin/env bash
# ==============================================================
# Multi-Domain & SSL Update Script
# İmza Gayrimenkul & Mahalle Domains
# ==============================================================

set -euo pipefail

echo "----------------------------------------------------"
echo "  Yeni Alan Adları İçin SSL ve Nginx Güncellemesi"
echo "----------------------------------------------------"

# 1. Nginx Kontrol ve Yapılandırma
echo "[1/4] Nginx kontrol ediliyor..."
if [ ! -d "/etc/nginx/sites-available" ]; then
    echo "Nginx dizinleri bulunamadı, Nginx kuruluyor veya dizinler oluşturuluyor..."
    sudo apt-get update && sudo apt-get install -y nginx
    sudo mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled
fi

echo "Nginx konfigürasyonu güncelleniyor..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
sudo ln -sf /etc/nginx/sites-available/imzagayrimenkul /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Nginx testi ve restart
sudo nginx -t && sudo systemctl reload nginx || sudo systemctl restart nginx

# 2. SSL Sertifikaları (imzaemlak.com)
echo "[2/4] imzaemlak.com için SSL sertifikası alınıyor..."
sudo certbot --nginx -d imzaemlak.com -d www.imzaemlak.com --non-interactive --agree-tos --email fatihselimkeskin@gmail.com --expand

# 3. SSL Sertifikaları (imzamahalle.com)
echo "[3/4] imzamahalle.com için SSL sertifikası alınıyor..."
sudo certbot --nginx -d imzamahalle.com -d www.imzamahalle.com --non-interactive --agree-tos --email fatihselimkeskin@gmail.com --expand

# 4. Final Restart
echo "[4/4] Nginx yeniden başlatılıyor..."
sudo systemctl reload nginx

echo "----------------------------------------------------"
echo "  ✅ İşlem Tamamlandı!"
echo "  Portal: https://imzaemlak.com"
echo "  Mahalle: https://imzamahalle.com"
echo "----------------------------------------------------"
