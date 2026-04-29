/**
 * İmza Gayrimenkul - Global Settings & Translation Handler
 * Manages Language (i18n), Currency, and Regional Visibility.
 */

async function changeLang(lang) {
    localStorage.setItem('imza_lang', lang);
    console.log('Language changed to:', lang);
    await initGlobalSettings();
}

function changeCurrency(curr) {
    localStorage.setItem('imza_currency', curr);
    console.log('Currency changed to:', curr);
    window.dispatchEvent(new CustomEvent('imzaCurrencyChanged', { detail: curr }));
}

async function initGlobalSettings() {
    const lang = localStorage.getItem('imza_lang') || 'tr';
    const curr = localStorage.getItem('imza_currency') || 'try';
    
    // Update select elements
    const langSelect = document.getElementById('langSelect');
    const currSelect = document.getElementById('currencySelect');
    
    if (langSelect) langSelect.value = lang;
    if (currSelect) currSelect.value = curr;

    // Apply RTL for Arabic
    if (lang === 'ar') {
        document.documentElement.setAttribute('dir', 'rtl');
        document.documentElement.lang = 'ar';
    } else {
        document.documentElement.setAttribute('dir', 'ltr');
        document.documentElement.lang = lang;
    }

    // Load and Apply Translations
    try {
        const response = await fetch(`/static/translations/${lang}.json`);
        if (response.ok) {
            const translations = await response.json();
            applyTranslations(translations);
        }
    } catch (e) {
        console.error('Translation error:', e);
    }
    
    console.log('İmza Settings Initialized:', { lang, curr });
    
    if (!localStorage.getItem('maybach_scroll')) {
        localStorage.setItem('maybach_scroll', 'enabled');
    }
}

function applyTranslations(t) {
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = t[key];
            } else {
                el.innerText = t[key];
            }
        }
    });
}

// Auto-init on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGlobalSettings);
} else {
    initGlobalSettings();
}
