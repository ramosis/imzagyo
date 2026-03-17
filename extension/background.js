chrome.runtime.onInstalled.addListener(() => {
  console.log("İmza Emlak Asistanı kuruldu! 🚀");
});

// --- YAPILANDIRMA (CONFIG) ---
const CONFIG = {
    // Canlı Sunucu (Google Cloud): https://imzaemlak.com
    // Yerel Test: http://127.0.0.1:8000
    API_BASE_URL: 'https://imzaemlak.com' 
};

// Arka plan işlemleri (Shadow Mode Sync)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "LOG_LISTING") {
    console.log("Dahili Senkronizasyon Başlatıldı:", request.data);
    
    // Flask API'ye gönder (Shadow Bridge)
    fetch(`${CONFIG.API_BASE_URL}/api/extension/sync`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request.data)
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP Hata! Statü: ${response.status}`);
        return response.json();
    })
    .then(data => {
        console.log("Sunucu Yanıtı:", data);
        sendResponse({ success: true, serverResponse: data });
    })
    .catch(error => {
        console.error("Senkronizasyon Hatası:", error);
        sendResponse({ success: false, error: error.message });
    });

    return true; // Asenkron yanıt için gerekli
  }
});
