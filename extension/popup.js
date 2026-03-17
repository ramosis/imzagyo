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
                const scrapeData = {
                    title: document.title,
                    price: document.querySelector('.classifiedInfoValue')?.innerText?.trim() || 
                           document.querySelector('.new-fiyat')?.innerText?.trim() || "Bilinmiyor",
                    url: window.location.href,
                    timestamp: new Date().toISOString()
                };
                return scrapeData;
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
