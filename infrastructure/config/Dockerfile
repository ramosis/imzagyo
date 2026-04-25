# Python tabanlı hafif bir imaj kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle (Gerekli temel paketler)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uploads ve DB için yazma izinlerini kontrol et
RUN mkdir -p uploads data && chmod -R 777 uploads data

# Uygulama portunu (8000) dışarı aç
EXPOSE 8000

# Healthcheck: Uygulama sağliğini kontrol et
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# Uygulamayı başlat
# Üretim ortamı için Gunicorn kullanıyoruz. 1GB RAM kısıtı nedeniyle 
# 1 adet Gevent worker kullanarak maksimum stabiliteyi sağlıyoruz.
CMD ["gunicorn", "-w", "1", "-k", "gevent", "-b", "0.0.0.0:8000", "wsgi:app"]
