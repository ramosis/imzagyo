# Veri Analitiği Modülü - Geliştirme Durumu

Karar destek mekanizmasının teknolojik kalbidir.

## Mevcut Özellikler (Tamamlananlar)
- [x] **L-Metrics Tracker:** `api/lmetrics.py` ile anonim ziyaretçi davranışı takibi.
- [x] **Veri Aggregasyonu:** Portföy izlenmeleri ve talep sayılarını raporlayan API'lar.
- [x] **Dashboard UI:** Özet kartlar ve anahtar metriklerin (KPI) gösterimi.

## Teknik Altyapı
- **Backend:** `api/lmetrics.py`, `api/finance.py`.
- **Frontend:** Chart.js, Leaflet.js (Isı haritası - planlanıyor).

## Gelecek Planları
- [ ] **AI Tahminleme:** Geçmiş verilere bakarak 3 ay sonrasının satış hacmini tahmin eden model.
- [ ] **Otomatik Rapor Gönderimi:** Yönetime her Pazartesi sabahı otomatik PDF rapor maili.
