/**
 * Evrensel ROI Asistanı - Content Script
 * NO-INJECT: DOM'a müdahale etmez, sadece veri okur.
 */

console.log("Evrensel ROI Asistanı Aktif 🥂");

/**
 * Sayfadaki verileri okur ve bir JSON objesi döner.
 */
function scrapeListingData() {
    const data = {
        title: document.title,
        price: "Bilinmiyor",
        m2: 0,
        rooms: "0+0",
        city: "",
        district: "",
        neighborhood: "",
        url: window.location.href // Sadece yerel karşılaştırma için kullanılır
    };

    // 1. JSON-LD (Schema.org) Analizi
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

    // 2. Jenerik Fiyat Tespiti (TL, USD, EUR etiketleri)
    if (data.price === "Bilinmiyor") {
        const pm = document.body.innerText.match(/(\d{1,3}(\.\d{3})*|(\d+))(\s*)(TL|₺|USD|€)/i);
        if (pm) data.price = pm[0];
    }

    // 3. Jenerik m2 Tespiti
    const m2Match = document.body.innerText.match(/(\d+)\s*(m2|metrekare)/i);
    if (m2Match) data.m2 = parseInt(m2Match[1]);

    // 4. Jenerik Oda Sayısı (Örn: 3+1, 2+1)
    const roomMatch = document.body.innerText.match(/(\d\+\d)/);
    if (roomMatch) data.rooms = roomMatch[1];

    // 5. Konum Tespiti (İpucu: Emlak siteleri genelde hiyerarşik adres kullanır)
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

// Mesaj dinleyici (Popup'tan tetiklenir)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "GET_LISTING_DATA") {
        sendResponse(scrapeListingData());
    }
});
