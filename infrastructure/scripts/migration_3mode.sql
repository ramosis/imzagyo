-- 1. Portföyler (Mülkler) tablosuna 'is_sample' sütunu ekleme
-- sqlite'da column_exists kontrolü olmadığı için try-catch benzeri bir yapı (aplikasyon katmanında) önerilir, 
-- Ancak SQL bazlı manuel çalışma için:
ALTER TABLE portfoyler ADD COLUMN is_sample BOOLEAN DEFAULT 0;

-- 2. Mevcut tüm ilanları 'Örnek' (Sample) olarak işaretleme
UPDATE portfoyler SET is_sample = 1;

-- 3. Sistem Ayarları (system_settings) tablosuna 'site_mode' ekleme
-- Modlar: 'demo' (Tümünü göster), 'placeholder' (Yer tutucu ekranı), 'live' (Sadece gerçek ilanlar)
INSERT OR IGNORE INTO system_settings (key, value, category, description) 
VALUES ('site_mode', 'placeholder', 'site', 'Site çalışma modu: demo, placeholder, live');

-- 4. Leads tablosuna 'segment' ve 'action_type' alanları ekleme (Lead form için)
-- Bazı versiyonlarda segment zaten var ise yoksayılacaktır.
ALTER TABLE leads ADD COLUMN segment TEXT; -- 'buyer', 'tenant', 'owner'
ALTER TABLE leads ADD COLUMN action_type TEXT; -- 'buy', 'rent', 'sell', 'lease'
