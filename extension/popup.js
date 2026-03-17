document.addEventListener('DOMContentLoaded', () => {
    const pageStatus = document.getElementById('pageStatus');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResult = document.getElementById('analysisResult');

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTab = tabs[0];
        if (activeTab.url.includes('sahibinden.com') || activeTab.url.includes('hepsiemlak.com') || activeTab.url.includes('zingat.com')) {
            pageStatus.innerText = "Emlak Sayfası Algılandı ✅";
            pageStatus.style.color = "#4ade80";
        } else if (activeTab.url.startsWith('http')) {
            pageStatus.innerText = "Yeni Site Algılandı (Jenerik) 🕵️‍♂️";
            pageStatus.style.color = "#fbbf24";
            analyzeBtn.disabled = false;
            analyzeBtn.style.opacity = "1";
        } else {
            pageStatus.innerText = "Desteklenmeyen Sayfa ❌";
            pageStatus.style.color = "#f87171";
            analyzeBtn.disabled = true;
            analyzeBtn.style.opacity = "0.5";
        }
    });

    analyzeBtn.addEventListener('click', async () => {
        analyzeBtn.innerText = "Analiz Ediliyor...";
        
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

        // Scripting API ile fonksiyonu direkt sayfaya enjekte et (Sessiz Mod)
        chrome.scripting.executeScript({
            target: { tabId: tab.id },
            func: () => {
                const url = window.location.href;
                const isSahibinden = url.includes('sahibinden.com');
                const isHepsiemlak = url.includes('hepsiemlak.com');
                const isZingat = url.includes('zingat.com');

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
                    data.price = document.querySelector('.classifiedInfoValue')?.innerText?.trim() || 
                                 document.querySelector('div.classifiedInfo > h3')?.innerText?.trim() || "Bilinmiyor";
                    const locationElements = document.querySelectorAll('.classifiedInfoValue');
                    if (locationElements.length >= 2) {
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

                    // Sahibinden Telefon
                    data.owner_phone = Array.from(document.querySelectorAll('.phone-numbers span, .phone-box'))
                                            .map(el => el.innerText.trim()).filter(t => t).join(' / ');
                    try {
                        const scripts = Array.from(document.querySelectorAll('script'));
                        const mapScript = scripts.find(s => s.textContent.includes('googleMapsData'));
                        if (mapScript) {
                            const latMatch = mapScript.textContent.match(/lat\s*:\s*([\d.]+)/);
                            const lngMatch = mapScript.textContent.match(/lon\s*:\s*([\d.]+)/);
                            if (latMatch) data.latitude = parseFloat(latMatch[1]);
                            if (lngMatch) data.longitude = parseFloat(lngMatch[1]);
                        }
                    } catch (e) {}
                } else if (isHepsiemlak) {
                    data.price = document.querySelector('.new-fiyat')?.innerText?.trim() || 
                                 document.querySelector('.price')?.innerText?.trim() || "Bilinmiyor";
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
                } else if (isZingat) {
                    // Zingat Fiyat
                    data.price = document.querySelector('.detail-price')?.innerText?.trim() || 
                                 document.querySelector('span[itemprop="price"]')?.innerText?.trim() || "Bilinmiyor";
                    
                    // Zingat Konum
                    const locPath = document.querySelector('.detail-location-path')?.innerText || "";
                    if (locPath) {
                        const parts = locPath.split(',').map(p => p.trim());
                        data.city = parts[0] || "";
                        data.district = parts[1] || "";
                        data.neighborhood = parts[2] || "";
                    }

                    // Zingat İlan Sahibi & Tarih
                    data.owner_name = document.querySelector('.agent-info .name')?.innerText?.trim() || 
                                      document.querySelector('.firm-name')?.innerText?.trim() || "";
                    
                    const detailList = document.querySelectorAll('.detail-info-list li');
                    detailList.forEach(li => {
                        if (li.innerText.includes("İlan Tarihi")) {
                            data.listing_date = li.innerText.replace("İlan Tarihi", "").trim();
                        }
                    });

                    // Zingat Telefon
                    data.owner_phone = Array.from(document.querySelectorAll('.agent-phone a'))
                                            .map(el => el.innerText.trim()).filter(t => t).join(' / ');

                    // Zingat Koordinat
                    try {
                        const mapContainer = document.querySelector('#map');
                        if (mapContainer) {
                            data.latitude = parseFloat(mapContainer.getAttribute('data-lat'));
                            data.longitude = parseFloat(mapContainer.getAttribute('data-lng'));
                        }
                    } catch (e) {}
                } else {
                    // --- JENERİK KAZIMA (Bilinmeyen Siteler) ---
                    const generic = (() => {
                        const res = { title: "", price: "Bilinmiyor", owner_name: "" };
                        try {
                            const scripts = document.querySelectorAll('script[type="application/ld+json"]');
                            scripts.forEach(s => {
                                try {
                                    const json = JSON.parse(s.textContent);
                                    const items = Array.isArray(json) ? json : (json['@graph'] || [json]);
                                    items.forEach(item => {
                                        if (item['@type'] === 'Product' || item['@type'] === 'RealEstateListing') {
                                            res.title = res.title || item.name || item.headline;
                                            if (item.offers) {
                                                const offer = Array.isArray(item.offers) ? item.offers[0] : item.offers;
                                                if (offer.price) res.price = `${offer.price} ${offer.priceCurrency || ''}`.trim();
                                            }
                                        }
                                    });
                                } catch (e) {}
                            });
                        } catch (e) {}
                        res.title = res.title || document.querySelector('meta[property="og:title"]')?.content || document.title;
                        if (res.price === "Bilinmiyor") {
                            const pm = document.body.innerText.match(/(\d{1,3}(\.\d{3})*|(\d+))(\s*)(TL|₺|USD|€)/i);
                            if (pm) res.price = pm[0];
                        }
                        return res;
                    })();
                    data.price = generic.price;
                    data.title = generic.title || data.title;
                    data.owner_name = generic.owner_name;
                }
                return data;
            }
        }, (results) => {
            if (results && results[0]) {
                const data = results[0].result;
                console.log("Yakalanan Veri:", data);
                
                // Arka plana bildir ve veritabanına yazılmasını bekle
                chrome.runtime.sendMessage({ action: "LOG_LISTING", data: data }, (response) => {
                    setTimeout(() => {
                        analyzeBtn.style.display = "none";
                        analysisResult.style.display = "block";
                        
                        if (response && response.success) {
                            pageStatus.innerText = "Veri Senkronize Edildi! ☁️";
                            pageStatus.style.color = "#D4AF37";
                        } else {
                            pageStatus.innerText = "Yerel Kaydedildi (Offline) ⚠️";
                            pageStatus.style.color = "#fbbf24";
                        }
                    }, 800);
                });
            } else {
                analyzeBtn.innerText = "Veri Okunamadı!";
            }
        });
    });
});
