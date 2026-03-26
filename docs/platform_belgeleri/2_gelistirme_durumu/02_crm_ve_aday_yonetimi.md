# CRM ve Aday Yönetimi Modülü - Geliştirme Durumu

Bu modül, platformun omurgasını oluşturan aday yönetim sistemidir.

## Mevcut Özellikler (Tamamlananlar)
- [x] **Pipeline API:** `api/pipeline.py` ile aday aşama yönetimi.
- [x] **Zaman Çizelgesi (Timeline):** Tüm verilerin (LMetrics, Saha Takip) tek bir flow'da birleşmesi.
- [x] **Atama Mantığı:** Gelen adayların müsaitlik durumuna göre danışmanlara atanması.

## Teknik Altyapı
- **Backend:** Flask Blueprint (`pipeline_bp`).
- **Frontend:** Sortable.js (Kanban sürükle-bırak için).
- **Veritabanı:** `leads`, `pipeline_history` tabloları.

## Gelecek Planları
- [ ] **AI Tahminleme:** Geçmiş satış verilerinden yola çıkarak "Satış Olasılığı" tahmini.
- [ ] **Email/SMS Sync:** CRM üzerinden doğrudan yazışma yapabilme.