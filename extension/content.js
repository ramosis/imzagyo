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
        m2_brut: 0,
        m2_net: 0,
        rooms: "0+0",
        city: "",
        district: "",
        neighborhood: "",
        listing_type: "Satılık", // Varsayılan
        category: "Daire",      // Varsayılan
        url: window.location.href 
    };

    const bodyText = document.body.innerText;

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

    // 2. Fiyat Tespiti 
    if (data.price === "Bilinmiyor") {
        const pm = bodyText.match(/(\d{1,3}(\.\d{3})*|(\d+))(\s*)(TL|₺|USD|€)/i);
        if (pm) data.price = pm[0];
    }

    // 3. m2 Tespiti (Net / Brüt Ayrımı)
    const m2Keywords = [
        { key: 'm2_brut', regex: /(Brüt|Toplam)\s*(Alan|m2|Metrekare)?\s*[:\s]*(\d+)/i },
        { key: 'm2_net', regex: /(Net|Kullanım)\s*(Alan|m2|Metrekare)?\s*[:\s]*(\d+)/i }
    ];

    m2Keywords.forEach(mk => {
        const match = bodyText.match(mk.regex);
        if (match) data[mk.key] = parseInt(match[3]);
    });

    // Eğer Brüt/Net bulunamadıysa jenerik m2 
    if (!data.m2_brut && !data.m2_net) {
        const genericM2 = bodyText.match(/(\d+)\s*(m2|metrekare)/i);
        if (genericM2) data.m2_brut = parseInt(genericM2[1]);
    }

    // 4. İlan Tipi (Satılık / Kiralık)
    if (bodyText.match(/Kiralık/i) || window.location.href.includes('kiralik')) {
        data.listing_type = "Kiralık";
    }

    // 5. Kategori Tespiti - Genişletilmiş liste
    const categories = [
        "Arsa", "Tarla", "Villa", "İşyeri", "Prefabrik", "Daire", "Rezidans",
        "Bahçe", "Çiftlik", "Ofis", "Depo", "Fabrika", "Dükkan", "Kompleks",
        "Yalı", "Köşk", "Bina", "Plaza", "Site", "Köyüstü", "Yatırımlık",
        "Turistik Tesis", "Otel", "Restoran", "Kafe", "Mağaza", "Salon",
        "Tesis", "Loft", "Penthouse", "Stüdyo", "Atölye", "Kültür Merkezi"
    ];
    
    // Önce başlıktan kontrol et
    for (const cat of categories) {
        if (data.title.includes(cat)) {
            data.category = cat;
            break;
        }
    }
    
    // Bulamadıysak body içeriğinden kontrol et
    if (data.category === "Daire") { // Varsayılan değerse
        for (const cat of categories) {
            if (bodyText.includes(cat)) {
                data.category = cat;
                break;
            }
        }
    }

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
