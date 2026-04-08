# İmza Gayrimenkul - Yerel Başlatma Scripti (Windows - Onarılmış Versiyon)
$host.UI.RawUI.WindowTitle = "İmza Gayrimenkul - Yerel Sunucu"

# Geçerli renkler: Black, DarkBlue, DarkGreen, DarkCyan, DarkRed, DarkMagenta, DarkYellow, Gray, DarkGray, Blue, Green, Cyan, Red, Magenta, Yellow, White
Write-Host "`n--- Yerel Ortam Hazırlanıyor ---" -ForegroundColor DarkYellow

# 1. Ortam Değişkenlerini Ayarla
$env:FLASK_DEBUG = "True"
$env:PORT = "8000"

# 2. Python Kontrolü
Write-Host "Python kontrol ediliyor..." -NoNewline
if (Get-Command "python" -ErrorAction SilentlyContinue) {
    Write-Host " [OK]" -ForegroundColor Green
} else {
    Write-Host " [HATA]" -ForegroundColor Red
    Write-Host "`n[!] Python bulunamadı! Lütfen Python'un yüklü ve PATH'e ekli olduğundan emin olun." -ForegroundColor Red
    Read-Host "`nÇıkmak için Enter'a basın..."
    exit
}

# 3. Sunucuyu Başlat
Write-Host "Uygulama başlatılıyor (http://localhost:8000)..." -ForegroundColor Cyan
Write-Host "Durdurmak için Ctrl+C tuşlarına basın.`n" -ForegroundColor Gray

python app.py

# Sunucu kapanırsa bekle
Write-Host "`n[!] Sunucu durduruldu." -ForegroundColor Red
Read-Host "Çıkmak için Enter'a basın..."
