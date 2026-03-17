document.addEventListener('DOMContentLoaded', () => {
    const pageStatus = document.getElementById('pageStatus');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResult = document.getElementById('analysisResult');

    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const activeTab = tabs[0];
        if (activeTab.url.includes('sahibinden.com') || activeTab.url.includes('hepsiemlak.com')) {
            pageStatus.innerText = "Emlak Sayfası Algılandı ✅";
            pageStatus.style.color = "#4ade80";
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

                const data = {
                    title: document.title,
                    price: "Bilinmiyor",
                    city: "",
                    district: "",
                    neighborhood: "",
                    latitude: null,
                    longitude: null,
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
