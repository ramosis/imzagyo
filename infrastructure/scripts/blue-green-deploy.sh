#!/bin/bash
set -e

ACTIVE=$(docker-compose ps | grep "Up" | grep "app_blue" > /dev/null && echo "blue" || echo "green")
INACTIVE=$([ "$ACTIVE" = "blue" ] && echo "green" || echo "blue")

echo "🔵 Active: $ACTIVE | 🟢 Deploying to: $INACTIVE"

# Deploy to inactive
docker-compose up -d app_$INACTIVE

# Health check
sleep 10
curl -f http://app_$INACTIVE:8000/health || {
    echo "❌ Health check failed, keeping $ACTIVE"
    docker-compose stop app_$INACTIVE
    exit 1
}

# Switch nginx upstream
sed -i "s/app_$ACTIVE/app_$INACTIVE/g" /etc/nginx/conf.d/upstream.conf
nginx -s reload

# Stop old
docker-compose stop app_$ACTIVE

echo "✅ Blue-green deployment complete. Active: $INACTIVE"
