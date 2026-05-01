#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Install dependencies
pip install -r requirements.txt

# Run migrations (eğer Alembic varsa)
# alembic upgrade head

# Run tests
pytest -q || { echo "❌ Tests failed"; exit 1; }

# Restart services
docker-compose -f infrastructure/config/docker-compose.prod.yml down
docker-compose -f infrastructure/config/docker-compose.prod.yml up -d --build

echo "✅ Deployment complete!"
