/**
 * Evrensel ROI Asistanı - Content Script
 */

console.log("Imza Insights HUD Aktif 🥂");

let hudContainer = null;

/**
 * Sayfayı analiz et ve HUD'ı başlat
 */
async function init() {
    const data = scrapeListingData();
    if (data && data.price !== "Bilinmiyor") {
        injectHUD();
        updateHUDWithLoading();
        
        // Background script aracılığıyla değerleme iste
        chrome.runtime.sendMessage({ action: "GET_VALUATION", data: data }, (response) => {
            if (response && !response.error) {
                renderHUDData(data, response);
            } else {
                renderHUDError(response?.error || "Bağlantı Hatası");
            }
        });
    }
}

function scrapeListingData() {
    const data = {
        title: document.title,
        price: "Bilinmiyor",
        m2_brut: 0,
        m2_net: 0,
        rooms: "0+0",
        city: "",
        district: "",
        neighborhood: "",
        listing_type: "Satılık",
        category: "Daire",
        url: window.location.href 
    };

    const bodyText = document.body.innerText;

    // JSON-LD Analizi
    try {
        const scripts = document.querySelectorAll('script[type="application/ld+json"]');
        scripts.forEach(s => {
            try {
                const json = JSON.parse(s.textContent);
                const items = Array.isArray(json) ? json : (json['@graph'] || [json]);
                items.forEach(item => {
                    if (item['@type'] === 'Product' || item['@type'] === 'RealEstateListing') {
                        data.title = item.name || item.headline || data.title;
                        if (item.offers) {
                            const offer = Array.isArray(item.offers) ? item.offers[0] : item.offers;
                            data.price = offer.price || data.price;
                        }
                    }
                });
            } catch (e) {}
        });
    } catch (e) {}

    // Fiyat Tespiti 
    if (data.price === "Bilinmiyor") {
        const pm = bodyText.match(/(\d{1,3}(\.\d{3})*|(\d+))(\s*)(TL|₺|USD|€)/i);
        if (pm) data.price = pm[0];
    }

    // m2 Tespiti
    const m2Match = bodyText.match(/(\d+)\s*(m2|metrekare)/i);
    if (m2Match) data.m2_brut = parseInt(m2Match[1]);

    // Konum Tespiti (Basit Breadcrumb asilimi)
    const breadcrumbs = Array.from(document.querySelectorAll('.breadcrumb li, .location-path li, .location a'))
                            .map(el => el.innerText.trim())
                            .filter(t => t.length > 2);
    
    if (breadcrumbs.length >= 3) {
        data.city = breadcrumbs[0];
        data.district = breadcrumbs[1];
        data.neighborhood = breadcrumbs[2];
    }

    return data;
}

function injectHUD() {
    if (document.getElementById('imza-hud')) return;

    hudContainer = document.createElement('div');
    hudContainer.id = 'imza-hud';
    hudContainer.className = 'imza-hud-container';
    document.body.appendChild(hudContainer);
}

function updateHUDWithLoading() {
    hudContainer.innerHTML = `
        <div class="imza-hud-header">🥂 Imza Insights</div>
        <div style="text-align: center; padding: 10px; font-size: 12px; color: #94A3B8;">
            AI Değerlemesi Yapılıyor...
        </div>
    `;
}

function renderHUDData(scraped, response) {
    const roiClass = response.roi_score > 5 ? 'success' : 'warning';
    
    hudContainer.innerHTML = `
        <div class="imza-hud-header">🥂 Imza Insights</div>
        <div class="imza-hud-row">
            <span class="imza-hud-label">AI Tahmini:</span>
            <span class="imza-hud-value">₺${response.predicted_price?.toLocaleString() || '---'}</span>
        </div>
        <div class="imza-hud-row">
            <span class="imza-hud-label">ROI Skoru:</span>
            <span class="imza-roi-badge">%${response.roi_score?.toFixed(2) || '0.00'}</span>
        </div>
        <div class="imza-hud-row">
            <span class="imza-hud-label">Piyasa Durumu:</span>
            <span class="imza-hud-value">${response.market_status || 'Dengeli'}</span>
        </div>
        <div class="imza-hud-row">
            <span class="imza-hud-label">Amortisman:</span>
            <span class="imza-hud-value">${response.amortization_years?.toFixed(1) || '---'} Yıl</span>
        </div>
        <button id="imza-hud-sync-btn" class="imza-hud-btn">Portala Aktar 🚀</button>
    `;

    document.getElementById('imza-hud-sync-btn').onclick = () => {
        chrome.runtime.sendMessage({action: "OPEN_POPUP"}); 
        // Not: Popup'ı programatik açmak zordur, genelde kullanıcıya "Popup'ı açın" mesajı verilir
        alert("Lütfen sağ üstteki eklenti ikonuna tıklayarak 'İmza Portala Gönder' butonuna basın.");
    };
}

function renderHUDError(error) {
    hudContainer.innerHTML = `
        <div class="imza-hud-header">🥂 Imza Insights</div>
        <div style="color: #F87171; font-size: 11px;">Hata: ${error}</div>
    `;
}

// Başlat
if (document.readyState === 'complete') {
    init();
} else {
    window.addEventListener('load', init);
}

// Mesaj dinleyici (Popup'tan tetiklenir)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "GET_LISTING_DATA") {
        sendResponse(scrapeListingData());
    }
});
