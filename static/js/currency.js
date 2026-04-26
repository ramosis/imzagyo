/**
 * İmza Currency Engine - Phase 2
 * Handles currency switching and price conversion.
 */

const currencyEngine = {
    currentCurrency: localStorage.getItem('imza_currency') || 'TRY',
    rates: { TRY: 1, USD: 0.030, EUR: 0.028 }, // Varsayılan/Yedek kurlar

    async init() {
        await this.fetchRates();
        this.apply();
        this.updateUI();
    },

    async fetchRates() {
        try {
            // Gerçek bir API'den kur çekilebilir (Örn: Fixer.io, ExchangeRate-API)
            // demo için şimdilik statik ama yapısı hazır.
            // const res = await fetch('https://api.exchangerate-api.com/v4/latest/TRY');
            // const data = await res.json();
            // this.rates = data.rates;
        } catch (err) {
            console.warn('Kur bilgisi çekilemedi, yedek kurlar kullanılıyor.');
        }
    },

    setCurrency(currency) {
        this.currentCurrency = currency;
        localStorage.setItem('imza_currency', currency);
        location.reload(); // Fiyatların yeniden hesaplanması için en temiz yöntem
    },

    formatPrice(priceTry) {
        const numericPrice = parseFloat(priceTry.replace(/[^0-9]/g, ''));
        if (isNaN(numericPrice)) return priceTry;

        const converted = numericPrice * this.rates[this.currentCurrency];
        
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: this.currentCurrency,
            maximumFractionDigits: 0
        });

        return formatter.format(converted).replace('TRY', '₺');
    },

    updateUI() {
        document.querySelectorAll('.currency-btn').forEach(btn => {
            if (btn.getAttribute('data-curr') === this.currentCurrency) {
                btn.classList.add('text-gold', 'font-bold');
            } else {
                btn.classList.remove('text-gold', 'font-bold');
            }
        });
    }
};

document.addEventListener('DOMContentLoaded', () => currencyEngine.init());
