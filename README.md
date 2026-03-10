# İmza Gayrimenkul - Web Application

Lüks gayrimenkul portföy yönetimi ve müşteri ilişkileri portalı.

## Proje Yapısı

Proje aşağıdaki ana bileşenlerden oluşmaktadır:

- **Root (/)**: Ana HTML dosyaları (`anasayfa.html`, `portal.html`, `koleksiyon.html` vb.) ve Flask uygulama dosyası (`app.py`).
- **api/**: Backend API servisleri (Flask Blueprints). Her modül kendi veri yönetiminden sorumludur.
  - `auth.py`: Giriş ve yetkilendirme işlemleri.
  - `portfolio.py`: Portföy ekleme, silme, güncelleme.
  - `users.py`: Kullanıcı yönetimi.
  - `contracts.py`, `taxes.py`, `maintenance.py`, `appointments.py`: PMS (Property Management System) modülleri.
- **scripts/**: Veritabanı ilklendirme, örnek veri yükleme ve HTML/JS enjeksiyonu gibi yardımcı araçlar.
- **uploads/**: Uygulama üzerinden yüklenen görsellerin saklandığı klasör.
- **css/**, **js/**, **images/**: Frontend statik dosyaları.

## Kurulum ve Çalıştırma

### Gereksinimler
- Python 3.x
- Flask
- SQLite3 (Python ile yerleşik gelir)

### Başlatma
1. Gerekli kütüphaneleri yükleyin (henüz yüklü değilse):
   ```bash
   pip install flask
   ```
2. Uygulamayı başlatın:
   ```bash
   python app.py
   ```
3. Tarayıcınızda `http://localhost:8000` adresine gidin.

## Admin Portalı

Portala erişim için `/portal.html` sayfasını kullanabilirsiniz. 

**Varsayılan Giriş Bilgileri:**
- Kullanıcı Adı: `admin`
- Şifre: `admin123`

## Veritabanı Yönetimi

Veritabanı otomatik olarak `app.py` ilk çalıştığında oluşturulur. Manuel sıfırlama veya örnek veri yükleme için `scripts/` altındaki dosyalar (root dizininden çalıştırılacak şekilde) kullanılabilir:

```bash
python scripts/fill_module_data.py
```

---
*İmza Gayrimenkul Yazılım Ekibi tarafından geliştirilmiştir.*

