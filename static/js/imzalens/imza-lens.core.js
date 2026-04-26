/**
 * İmza Lens - Core Engine (imza-lens.core.js)
 * Akıllı Karşılama, Niyet Takibi ve Profil Zenginleştirme Çekirdeği
 * (c) 2026 İmza Gayrimenkul Yatırım
 */

const ImzaLens = {
    VERSION: '1.3',
    // Veri Saklama Anahtarları
    KEYS: {
        INTERESTS: 'imza_interests',
        PROFILE: 'imza_lens_profile'
    },

    // 1. DİJİTAL İZ TAKİBİ (Tracking)
    // Kullanıcının ilgi alanlarını ve davranışlarını sessizce kaydeder.
    track(collection, price = 0) {
        try {
            let interests = JSON.parse(localStorage.getItem(this.KEYS.INTERESTS) || '[]');
            interests.push({ 
                collection: collection, 
                price: price, 
                time: Date.now(),
                path: window.location.pathname
            });
            // Son 30 etkileşimi tut (Profil derinliği için ideal)
            if (interests.length > 30) interests = interests.slice(-30);
            localStorage.setItem(this.KEYS.INTERESTS, JSON.stringify(interests));
            console.log(`[İmza Lens] İz Senkronize Edildi: ${collection}`);
        } catch (e) {
            console.warn('[İmza Lens] İz kaydedilemedi:', e);
        }
    },

    // 2. ANALİZ (Analysis)
    // Toplanan verileri anlamlandırıp kullanıcının "Gayrimenkul Karakterini" belirler.
    getTopInterest() {
        const interests = JSON.parse(localStorage.getItem(this.KEYS.INTERESTS) || '[]');
        if (interests.length === 0) return null;
        const counts = {};
        interests.forEach(i => { counts[i.collection] = (counts[i.collection] || 0) + 1; });
        return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
    },

    getIntent() {
        const urlParams = new URLSearchParams(window.location.search);
        const referrer = document.referrer.toLowerCase();
        const topInterest = this.getTopInterest();

        // 1. Niyet (URL/Parametre) - En güçlü kanıt
        if (urlParams.has('tip') && urlParams.get('tip') === 'kiralik') return 'kiralik';
        if (urlParams.has('koleksiyon') && urlParams.get('koleksiyon') === 'arsa') return 'arsa';
        if (urlParams.has('tip') && urlParams.get('tip') === 'satilik') return 'satilik';
        
        // 2. Referrer (Google/Sosyal Medya) - Geliş kapısı analizi
        if (referrer.includes('google')) return 'konut';
        if (referrer.includes('instagram') || referrer.includes('facebook')) return 'prestij';

        // 3. Davranışsal Tahmin (LocalStorage)
        return topInterest || 'konut';
    },

    // 3. GEO-TARGETING (Konum Tespiti)
    // Kullanıcının nereden geldiğini saptayıp yerelleştirilmiş selamlar sunar.
    async detectLocation() {
        const cachedGeo = localStorage.getItem('imza_lens_geo');
        if (cachedGeo) {
            const data = JSON.parse(cachedGeo);
            // 24 saatlik cache ömrü
            if (Date.now() - data.detectedAt < 86400000) return data;
        }

        try {
            const response = await fetch('https://freeipapi.com/api/json');
            const data = await response.json();
            if (data.cityName) {
                const geoData = {
                    city: data.cityName,
                    country: data.countryName,
                    ip: data.ipAddress,
                    detectedAt: Date.now()
                };
                localStorage.setItem('imza_lens_geo', JSON.stringify(geoData));
                console.log(`[İmza Lens] Lokasyon Saptandı: ${data.cityName}`);
                return geoData;
            }
        } catch (e) {
            console.warn('[İmza Lens] Lokasyon tespiti yapılamadı:', e);
        }
        return null;
    },

    // 4. PROFİL ZENGİNLEŞTİRME (Lead Enrichment Export)
    getLeadData() {
        const geo = JSON.parse(localStorage.getItem('imza_lens_geo') || '{}');
        return {
            source: document.referrer || 'Direct Search',
            topInterest: this.getTopInterest(),
            recentIntent: this.getIntent(),
            location: geo.city || 'Belirlenemedi',
            visitPathCount: JSON.parse(localStorage.getItem(this.KEYS.INTERESTS) || '[]').length,
            detectedAt: new Date().toISOString()
        };
    },
    // 5. SHADOW BRIDGE (Veri Senkronizasyonu)
    // Anonim verileri yönetici paneli (CRM) için sunucuya iletir.
    getShadowId() {
        let id = localStorage.getItem('imza_shadow_id');
        if (!id) {
            id = 'shd_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
            localStorage.setItem('imza_shadow_id', id);
        }
        return id;
    },

    async syncShadowBridge() {
        const shadowId = this.getShadowId();
        const metrics = JSON.parse(localStorage.getItem('imza_lens_metrics_v2') || '{}');
        const geo = JSON.parse(localStorage.getItem('imza_lens_geo') || '{}');
        
        try {
            const response = await fetch('/api/tracking/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    shadow_id: shadowId,
                    metrics: metrics,
                    geo: geo
                })
            });
            const result = await response.json();
            console.log(`[İmza Lens] Shadow Bridge Senkronize: ${result.status}`);
        } catch (e) {
            console.warn('[İmza Lens] Shadow Bridge senkronizasyon hatası:', e);
        }
    }
};

// Otomatik Başlatma & Periyodik Senkronizasyon
console.log(`[İmza Lens] Core v${ImzaLens.VERSION} Başlatılıyor...`);
ImzaLens.detectLocation();
setInterval(() => ImzaLens.syncShadowBridge(), 60000); // Her dakikada bir otomatik senkronize et
window.addEventListener('pagehide', () => ImzaLens.syncShadowBridge()); // Sayfadan ayrılırken son bir kez gönder

// Global Erişilebilirlik
window.ImzaLens = ImzaLens;
console.log('[İmza Lens] Global Nesne Hazır.');
