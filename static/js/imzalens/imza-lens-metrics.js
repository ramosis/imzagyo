/**
 * İmza Lens - Luxury Metrics (imza-lens-metrics.js)
 * Davranışsal Derinlik Analizi ve Etkileşim Kalite Skorlama
 * (c) 2026 İmza Gayrimenkul Yatırım
 */

const ImzaLensMetrics = {
    config: {
        minFocusTime: 2000, // 2 saniye altındaki bakışlar "yüzeysel" sayılır
        scrollThrottle: 150,
        keys: {
            METRICS: 'imza_lens_metrics_v2'
        }
    },

    state: {
        maxScrollDepth: 0,
        focusStarts: {},
        interactions: []
    },

    init() {
        console.log('[İmza Lens Metrics] Aktive edildi. Derinlik analizi başlıyor...');
        this.bindEvents();
    },

    bindEvents() {
        // 1. Scroll Derinliği Takibi (Throttled + Hybrid Events)
        const depthCheck = () => {
            if (!this.state.scrollTimeout) {
                this.state.scrollTimeout = setTimeout(() => {
                    this.calculateScrollDepth();
                    this.state.scrollTimeout = null;
                }, this.config.scrollThrottle);
            }
        };

        window.addEventListener('scroll', depthCheck);
        window.addEventListener('wheel', depthCheck);
        window.addEventListener('keydown', (e) => {
            if (['ArrowDown', 'ArrowUp', 'PageDown', 'PageUp', 'Space'].includes(e.key)) {
                depthCheck();
            }
        });
        window.addEventListener('touchmove', depthCheck);

        // Periyodik kontrol (Sigorta mekanizması)
        setInterval(depthCheck, 2000);

        // 2. Görsel Odaklanma Takibi (Hover Depth)
        document.addEventListener('mouseover', (e) => {
            const trackable = e.target.closest('[data-imza-lens-track]');
            if (trackable) {
                const id = trackable.getAttribute('data-imza-lens-track');
                this.state.focusStarts[id] = Date.now();
            }
        });

        document.addEventListener('mouseout', (e) => {
            const trackable = e.target.closest('[data-imza-lens-track]');
            if (trackable) {
                const id = trackable.getAttribute('data-imza-lens-track');
                if (this.state.focusStarts[id]) {
                    const focusDuration = Date.now() - this.state.focusStarts[id];
                    if (focusDuration >= this.config.minFocusTime) {
                        this.logInteraction('focus', id, focusDuration);
                    }
                    delete this.state.focusStarts[id];
                }
            }
        });

        // 3. Sayfa Terk Edilirken Veriyi Kaydet
        window.addEventListener('beforeunload', () => {
            this.saveFinalMetrics();
        });
    },

    calculateScrollDepth() {
        // 1. Geleneksel Scroll Ölçümü
        const winHeight = window.innerHeight;
        const docHeight = document.documentElement.scrollHeight;
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        let traditionalDepth = Math.round(((scrollTop + winHeight) / docHeight) * 100);

        // 2. Maybach Scroll (Section-based) Ölçümü
        // Eğer sayfada currentSectionIndex varsa (global olarak anasayfa.html'de tanımlı)
        let sectionDepth = 0;
        if (typeof currentSectionIndex !== 'undefined' && typeof sections !== 'undefined') {
            sectionDepth = Math.round(((currentSectionIndex + 1) / sections.length) * 100);
        }

        // Hibrit Karar: Hangisi daha büyükse o derinliktir (İmza Lens Stratejisi)
        const depth = Math.max(traditionalDepth, sectionDepth);

        if (depth > this.state.maxScrollDepth) {
            this.state.maxScrollDepth = depth;
            if (depth >= 25 && depth % 25 === 0) { // Her %25'lik dilimde logla
                this.logInteraction('scroll_milestone', 'depth', depth);
            }
        }
    },

    logInteraction(type, target, value) {
        const interaction = {
            type,
            target,
            value,
            timestamp: Date.now(),
            url: window.location.pathname
        };
        this.state.interactions.push(interaction);
        
        // Eğer İmzaLens Core yüklüyse, ona da haber ver (Lead Enrichment için)
        if (window.ImzaLens && type === 'focus') {
            window.ImzaLens.track(target, 0); // Odaklanılan kategoriyi ilgi alanı olarak işle
        }
        
        console.log(`[L-Metrics] ${type} -> ${target}: ${value}`);
    },

    calculateQualityScore() {
        let score = 0;
        
        // Scroll Derinliği Puanı (Max 40 puan)
        score += (this.state.maxScrollDepth * 0.4);

        // Odaklanma Puanı (Her kaliteli görsel odağı +10 puan, Max 40 puan)
        const focusCount = this.state.interactions.filter(i => i.type === 'focus').length;
        score += Math.min(40, focusCount * 10);

        // Zaman Puanı (Eğer sayfa 30 saniyeden fazla incelenmişse +20 puan)
        // Bu ölçüm için sayfa yükleme zamanı kullanılabilir
        
        return Math.round(score);
    },

    saveFinalMetrics() {
        const metrics = {
            maxDepth: this.state.maxScrollDepth,
            qualityScore: this.calculateQualityScore(),
            interactionsCount: this.state.interactions.length,
            sessionEnd: Date.now()
        };
        localStorage.setItem(this.config.keys.METRICS, JSON.stringify(metrics));
    },

    getMetrics() {
        return {
            maxDepth: this.state.maxScrollDepth,
            qualityScore: this.calculateQualityScore(),
            interactions: this.state.interactions.length,
            sessionDuration: Date.now() - (this.state.sessionStart || Date.now())
        };
    }
};

// Global Başlatma
document.addEventListener('DOMContentLoaded', () => {
    ImzaLensMetrics.state.sessionStart = Date.now();
    ImzaLensMetrics.init();
});
window.ImzaLensMetrics = ImzaLensMetrics;
