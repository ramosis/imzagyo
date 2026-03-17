chrome.runtime.onInstalled.addListener(() => {
  console.log("İmza Emlak Asistanı kuruldu! 🚀");
});

// Arka plan işlemleri (Shadow Mode Sync)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "LOG_LISTING") {
    console.log("Dahili Senkronizasyon Başlatıldı:", request.data);
    
    // Flask API'ye gönder (Shadow Bridge)
    fetch('http://127.0.0.1:5000/api/extension/sync', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(request.data)
    })
    .then(response => response.json())
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
