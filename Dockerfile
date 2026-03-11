# Python tabanlı hafif bir imaj kullanıyoruz
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle (SQLite ve diğer araçlar için gerekirse)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Uploads ve DB için yazma izinlerini kontrol et (Unix tabanlı sistemlerde gerekebilir)
RUN mkdir -p uploads && chmod -R 777 uploads

# Uygulama portunu (8000) dışarı aç
EXPOSE 8000

# Uygulamayı başlat
# Gunicorn veya benzeri bir WSGI sunucu prodüksiyon için daha iyidir, 
# ancak şimdilik flask'in kendi sunucusunu (debug=False) kullanabiliriz.
CMD ["python", "app.py"]
