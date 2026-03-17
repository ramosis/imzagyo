console.log("İmza Emlak Asistanı aktif! 🕵️‍♂️");

// --- YARDIMCI SCRAPER FONKSİYONLARI ---
function scrapeListingData() {
    const url = window.location.href;
    const isSahibinden = url.includes('sahibinden.com');
    const isHepsiemlak = url.includes('hepsiemlak.com');

    const data = {
        title: document.title,
        price: "Bilinmiyor",
        city: "",
        district: "",
        neighborhood: "",
        latitude: null,
        longitude: null,
        url: url,
        timestamp: new Date().toISOString()
    };

    if (isSahibinden) {
        // Sahibinden Fiyat
        data.price = document.querySelector('.classifiedInfoValue')?.innerText?.trim() || 
                     document.querySelector('div.classifiedInfo > h3')?.innerText?.trim() || "Bilinmiyor";
        
        // Sahibinden Konum (İl/İlçe/Mahalle)
        const locationElements = document.querySelectorAll('.classifiedInfoValue');
        if (locationElements.length >= 2) {
            // Genelde İlçe/İl formatı veya birleşik
            const locText = locationElements[1]?.innerText || "";
            const parts = locText.split('/').map(p => p.trim());
            data.city = parts[0] || "";
            data.district = parts[1] || "";
            data.neighborhood = parts[2] || "";
        }

        // Sahibinden Koordinat (Script içinden çekme)
        try {
            const scripts = Array.from(document.querySelectorAll('script'));
            const mapScript = scripts.find(s => s.textContent.includes('googleMapsData'));
            if (mapScript) {
                const latMatch = mapScript.textContent.match(/lat\s*:\s*([\d.]+)/);
                const lngMatch = mapScript.textContent.match(/lon\s*:\s*([\d.]+)/);
                if (latMatch) data.latitude = parseFloat(latMatch[1]);
                if (lngMatch) data.longitude = parseFloat(lngMatch[1]);
            }
        } catch (e) { console.warn("Koordinat çekilemedi:", e); }

        // Sahibinden ROI / Kira Tahmini (Emlak Endeksi widget'ı varsa)
        try {
            const rentText = document.querySelector('.re-valuation-info-value')?.innerText || "";
            if (rentText) {
                const rentMatch = rentText.match(/([\d.]+)/);
                if (rentMatch) data.estimated_rent = parseFloat(rentMatch[1].replace(/\./g, ''));
            }
        } catch (e) {}

    } else if (isHepsiemlak) {
        // Hepsiemlak Fiyat
        data.price = document.querySelector('.new-fiyat')?.innerText?.trim() || 
                     document.querySelector('.price')?.innerText?.trim() || "Bilinmiyor";
        
        // Hepsiemlak Konum
        const locParts = document.querySelectorAll('.detay-konum .short-info');
        if (locParts.length > 0) {
            const locText = locParts[0].innerText || "";
            const parts = locText.split(',').map(p => p.trim());
            data.city = parts[0] || "";
            data.district = parts[1] || "";
            data.neighborhood = parts[2] || "";
        }
    }

    return data;
}

// Popup'tan gelen talepleri dinle
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "ANALYZE_PAGE") {
        const listingData = scrapeListingData();
        
        // Veriyi arka plana da gönder (Shadow Mode Log)
        chrome.runtime.sendMessage({ action: "LOG_LISTING", data: listingData });
        
        sendResponse({ success: true, data: listingData });
    }
});
