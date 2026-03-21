#!/usr/bin/env bash
# ==============================================================
# Deployment Setup Script
# İmza Gayrimenkul Portal — Production Server Setup
# ==============================================================
# Run this script on a fresh Ubuntu 22.04+ server as root or via sudo.
# It will:
#   1. Install system dependencies (Nginx, Certbot, Python3, pip)
#   2. Create the app directory and virtual environment
#   3. Install Python dependencies
#   4. Copy Nginx config and systemd service
#   5. Obtain an SSL certificate via Certbot
#   6. Enable automatic SSL renewal via systemd timer
#   7. Start the application
# ==============================================================

set -euo pipefail

# --- Configuration ---
DOMAIN="${1:-imzagayrimenkul.com}"
APP_DIR="/imzagyo"
CERTBOT_WEBROOT="/var/www/certbot"
EMAIL="${2:-admin@$DOMAIN}"

echo "=============================================="
echo "  İmza Gayrimenkul — Production Setup"
echo "  Domain : $DOMAIN"
echo "  Email  : $EMAIL"
echo "=============================================="

# --- 1. System Packages ---
echo "[1/7] Installing system packages..."
apt-get update -y
apt-get install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx ufw

# --- 2. App Directory & Virtual Env ---
echo "[2/7] Setting up application directory..."
mkdir -p "$APP_DIR" "$CERTBOT_WEBROOT"
cp -r . "$APP_DIR/" 2>/dev/null || true
cd "$APP_DIR"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors gunicorn

# --- 3. Nginx Configuration ---
echo "[3/7] Configuring Nginx reverse proxy..."
cp deploy/nginx.conf /etc/nginx/sites-available/imzagayrimenkul
ln -sf /etc/nginx/sites-available/imzagayrimenkul /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

# --- 4. Firewall ---
echo "[4/7] Configuring firewall..."
ufw allow 'Nginx Full'
ufw allow OpenSSH
ufw --force enable

# --- 5. SSL Certificate ---
echo "[5/7] Obtaining SSL certificate..."
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m "$EMAIL"

# --- 6. Systemd Service ---
echo "[6/7] Installing systemd service..."
cp deploy/imzagayrimenkul.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable imzagayrimenkul

# --- 7. SSL Auto-Renewal (cron) ---
echo "[7/7] Setting up automatic SSL renewal..."
cp deploy/renew_ssl.sh /usr/local/bin/renew_ssl_imza.sh
chmod +x /usr/local/bin/renew_ssl_imza.sh

# Add cron job: run daily at 02:30 AM
(crontab -l 2>/dev/null; echo "30 2 * * * /usr/local/bin/renew_ssl_imza.sh") | crontab -

# --- Start the Application ---
echo "Starting application..."
systemctl start imzagayrimenkul

echo ""
echo "=============================================="
echo "  ✅ Deployment complete!"
echo "  Portal: https://$DOMAIN"
echo "  SSL renewal: daily at 02:30 via cron"
echo "  Service: systemctl status imzagayrimenkul"
echo "=============================================="
