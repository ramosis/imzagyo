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
        owner_name: "",
        owner_phone: "",
        listing_date: "",
        url: url,
        listing_type: url.includes('kiralik') ? 'Kiralık' : 'Satılık',
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

        // Sahibinden İlan Sahibi & Tarih
        data.owner_name = document.querySelector('.username')?.innerText?.trim() || 
                          document.querySelector('.site-buyer-info .username')?.innerText?.trim() || "";
        
        const infoList = document.querySelectorAll('.classifiedInfoList li');
        infoList.forEach(li => {
            const label = li.querySelector('strong')?.innerText || "";
            if (label.includes("İlan Tarihi")) {
                data.listing_date = li.querySelector('span')?.innerText?.trim() || "";
            }
        });

        // Sahibinden Telefon (DOM'da varsa)
        data.owner_phone = Array.from(document.querySelectorAll('.phone-numbers span, .phone-box'))
                                .map(el => el.innerText.trim()).filter(t => t).join(' / ');

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

        // Hepsiemlak İlan Sahibi & Tarih
        data.owner_name = document.querySelector('.owner-info .name')?.innerText?.trim() || 
                          document.querySelector('.firm-name')?.innerText?.trim() || "";
        
        const detailItems = document.querySelectorAll('.detay-liste li');
        detailItems.forEach(li => {
            if (li.innerText.includes("İlan Tarihi")) {
                data.listing_date = li.innerText.replace("İlan Tarihi", "").trim();
            }
        });

        // Hepsiemlak Telefon
        data.owner_phone = Array.from(document.querySelectorAll('.phone-numbers'))
                                .map(el => el.innerText.trim()).filter(t => t).join(' / ');

        // Hepsiemlak Koordinat (Map elementinden veya scripts)
        try {
            const mapEl = document.querySelector('#map');
            if (mapEl) {
                data.latitude = parseFloat(mapEl.getAttribute('data-lat'));
                data.longitude = parseFloat(mapEl.getAttribute('data-lng'));
            }
            if (!data.latitude) {
                const scriptText = Array.from(document.querySelectorAll('script')).find(s => s.textContent.includes('centerLat'))?.textContent || "";
                const latMatch = scriptText.match(/centerLat\s*:\s*([\d.]+)/);
                const lngMatch = scriptText.match(/centerLng\s*:\s*([\d.]+)/);
                if (latMatch) data.latitude = parseFloat(latMatch[1]);
                if (lngMatch) data.longitude = parseFloat(lngMatch[1]);
            }
        } catch (e) {}
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
