#!/usr/bin/env bash
# ==============================================================
# SSL Certificate Auto-Renewal Script
# İmza Gayrimenkul Portal
# ==============================================================
# This script is meant to be called by a cron job or systemd timer.
# It renews the Let's Encrypt certificate via Certbot,
# restarts Nginx to pick up the new cert, and logs the result.
# ==============================================================

set -euo pipefail

LOG_FILE="/var/log/imza_ssl_renew.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] Starting SSL certificate renewal..." >> "$LOG_FILE"

# Attempt renewal
if certbot renew --quiet --deploy-hook "systemctl reload nginx"; then
    echo "[$TIMESTAMP] SSL renewal completed successfully." >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] SSL renewal failed (may not be due yet; check certbot logs)." >> "$LOG_FILE"
fi

echo "[$TIMESTAMP] Done." >> "$LOG_FILE"
