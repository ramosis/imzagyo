# Kütahya Örnek Veri Modülü Tasarımı (Sample Data Module)

Bu plan, sitenin ilk kurulumda dolu görünmesini sağlamak amacıyla Kütahya ve ilçelerine özel 15+ örnek ilan, ekip ve esnaf verisi eklenmesini ve bunların yönetimini kapsar.

## 1. Veritabanı Mimarisi

Mevcut tabloların (portfoyler, ekip, businesses, hero_slides) her birine şu kolon eklenecektir:
- `is_sample` (BOOLEAN, DEFAULT 0): Verinin örnek (dummy) olup olmadığını belirtir.

Ayrıca `system_settings` veya mevcut `settings.py` üzerinden yönetilecek yeni bir global ayar eklenecektir:
- `show_sample_data` (BOOLEAN): Örnek verilerin frontend'de gösterilip gösterilmeyeceğini kontrol eder.

## 2. Örnek Veri Havuzu (15+ İlan)

Aşağıdaki lokasyon dağılımına göre gerçekçi ama örnek veriler üretilecektir:

| Lokasyon | Tip | Adet | Önemli Noktalar |
| :--- | :--- | :--- | :--- |
| Kütahya Merkez | Daire/Rezidans | 6 | Sera AVM, Vazo Meydanı, Zafertepe, Meydan |
| Tavşanlı | Müstakil Ev/Arsa | 4 | Hanımçeşme, Çırçır mevkii, Yeni Mahalle |
| Simav | Termal Arsa/Villa | 3 | Eynal Kaplıcaları civarı |
| Emet | Daire/Arsa | 2 | Kaplıcalar bölgesi, Merkez |
| Gediz | Ticari/Daire | 2 | Merkez, Murat Dağı yolu |

## 3. Ekip ve Mahalle Rehberi

- **Ekip:** "Kütahya Bölge Sorumlusu" ve "Tavşanlı Şube Danışmanı" gibi 2-3 adet profil.
- **Esnaf (İmza Mahalle):** 
    - Kütahya Porselen Mağazası (Örnek)
    - Yerel Tesisatçı (Merkez)
    - Anahtarcı (Tavşanlı)
    - Yerel Fırın (Simav)

## 4. Yönetim Özellikleri (Portal/Admin)

Admin panelinde "Sistem Ayarları" altında yeni bir widget oluşturulacaktır:
- **[Toggle] Örnek Verileri Göster:** Açık olduğunda `is_sample=1` verileri API sonuçlarına dahil edilir.
- **[Button] Örnek Verileri Temizle:** Veritabanındaki tüm `is_sample=1` kayıtlarını kalıcı olarak siler.
- **Otomatik Gizleme Kuralı:** Gerçek (is_sample=0) ilan sayısı 10'u geçtiğinde, örnek ilanlar listenin en sonuna atılır veya isteğe bağlı olarak otomatik gizlenir.

## 5. API Entegrasyonu

`app.py` ve ilgili API uç noktalarında sorgu şu şekilde güncellenecektir:
```sql
SELECT * FROM portfoyler 
WHERE (is_sample = 0 OR (is_sample = 1 AND :show_sample_data = 1))
ORDER BY is_sample ASC, created_at DESC
```

## 6. Uygulama Sırası (Roadmap)

1. [ ] Migration: Tablolara `is_sample` kolonunun eklenmesi.
2. [ ] Data: `database.py` içinde 15+ Kütahya verisinin tanımlanması.
3. [ ] Logic: API'lerin (Portfolio, Team, Neighborhood) örnek veri mantığına göre güncellenmesi.
4. [ ] UI: Portal sayfasına yönetim kontrollerinin eklenmesi.
5. [ ] Test: Gerçek veri eklendiğinde örnek verilerin davranışının kontrolü.
