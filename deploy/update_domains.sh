#!/usr/bin/env bash
# ==============================================================
# Multi-Domain & SSL Update Script
# İmza Gayrimenkul & Mahalle Domains
# ==============================================================

set -euo pipefail

echo "----------------------------------------------------"
echo "  Yeni Alan Adları İçin SSL ve Nginx Güncellemesi"
echo "----------------------------------------------------"

# 1. Nginx Konfigürasyonunu Kopyala
echo "[1/4] Nginx konfigürasyonu güncelleniyor..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
sudo ln -sf /etc/nginx/sites-available/imzagayrimenkul /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 2. SSL Sertifikaları (imzaemlak.com)
echo "[2/4] imzaemlak.com için SSL sertifikası alınıyor..."
sudo certbot --nginx -d imzaemlak.com -d www.imzaemlak.com --non-interactive --agree-tos --expand

# 3. SSL Sertifikaları (imzamahalle.com)
echo "[3/4] imzamahalle.com için SSL sertifikası alınıyor..."
sudo certbot --nginx -d imzamahalle.com -d www.imzamahalle.com --non-interactive --agree-tos --expand

# 4. Final Restart
echo "[4/4] Nginx yeniden başlatılıyor..."
sudo systemctl reload nginx

echo "----------------------------------------------------"
echo "  ✅ İşlem Tamamlandı!"
echo "  Portal: https://imzaemlak.com"
echo "  Mahalle: https://imzamahalle.com"
echo "----------------------------------------------------"
