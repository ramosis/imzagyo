/**
 * İmza I18n Engine - Phase 2
 * Handles multi-language switching and UI updates.
 */

const i18n = {
    currentLang: localStorage.getItem('imza_lang') || 'tr',
    translations: {},

    async init() {
        try {
            const response = await fetch('../data/translations.json');
            this.translations = await response.json();
            this.apply();
            this.updateDirection();
        } catch (err) {
            console.warn('I18n Yükleme Hatası (translations.json bulunamadı veya TR aktif)', err);
        }
    },

    getLang() {
        return this.currentLang;
    },

    setLanguage(lang) {
        this.currentLang = lang;
        localStorage.setItem('imza_lang', lang);
        // Sayfayı yenilemek en güvenli yöntem (SEO ve API verileri için)
        window.location.reload(); 
    },

    apply() {
        const trans = this.translations[this.currentLang];
        if (!trans) return;

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (trans[key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = trans[key];
                } else {
                    el.innerText = trans[key];
                }
            }
        });
    },

    updateDirection() {
        // Arapça için sağdan sola (RTL) desteği
        if (this.currentLang === 'ar') {
            document.documentElement.dir = 'rtl';
            document.documentElement.lang = 'ar';
        } else {
            document.documentElement.dir = 'ltr';
            document.documentElement.lang = this.currentLang;
        }
    }
};

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => i18n.init());
