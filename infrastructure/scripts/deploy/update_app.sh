#!/usr/bin/env bash
# ==============================================================
# İmza Gayrimenkul Akıllı Güncelleme Scripti (v1.0)
# ==============================================================

set -e # Bir hata oluşursa scripti durdur

echo "----------------------------------------------------"
echo "  🚀 İmza Gayrimenkul Güncelleme Başlatıldı"
echo "----------------------------------------------------"

# 1. Klasör ve Git Güncelleme
echo "[1/4] Kodlar GitHub'dan çekiliyor..."
cd /opt/imzagyo
sudo git fetch --all && sudo git reset --hard origin/main

# 1.1 Veritabanı İndekslemesi (Performans için)
echo "[1.1/4] Veritabanı performans indeksleri oluşturuluyor..."
sudo python3 scripts/optimize_db.py || echo "⚠️ İndeksleme atlandı (Hata veya dosya yok)"

# 2. Docker Konteyner Temizliği (Port Çakışmasını Önlemek İçin)
echo "[2/4] Eski kalıntılar temizleniyor..."
sudo docker-compose down --remove-orphans

# 3. Yeniden Derleme ve Başlatma
echo "[3/4] Konteynerler yeniden derleniyor (Build)..."
if sudo docker-compose up -d --build; then
    echo "✅ Konteynerler başarıyla ayağa kalktı."
else
    echo "❌ HATA: Derleme sırasında bir sorun oluştu!"
    sudo docker-compose logs --tail=20
    exit 1
fi

# 4. Sağlık Kontrolü (Health Check)
echo "[4/4] Uygulama sağlığı kontrol ediliyor (20 saniye bekleniyor)..."
sleep 20

# Durumu kontrol et
STATUS=$(sudo docker inspect -f '{{.State.Health.Status}}' imza-backend 2>/dev/null || echo "not-found")

if [ "$STATUS" == "healthy" ]; then
    echo "----------------------------------------------------"
    echo "  ✨ BAŞARILI: Sistem şu an yayında ve sağlıklı!"
    echo "  Portal: https://imzaemlak.com"
    echo "  Mahalle: https://imzamahalle.com"
    echo "----------------------------------------------------"
elif [ "$STATUS" == "starting" ]; then
    echo "----------------------------------------------------"
    echo "  ⏳ UYARI: Uygulama hala başlıyor..."
    echo "  Lütfen 1-2 dakika sonra tarayıcıyı yenileyin."
    echo "----------------------------------------------------"
else
    echo "----------------------------------------------------"
    echo "  ❌ KRİTİK HATA: Uygulama başlayamadı!"
    echo "  Son 20 satır log (Hata sebebi burada yazar):"
    echo "----------------------------------------------------"
    sudo docker logs imza-backend --tail 50
fi
