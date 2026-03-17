console.log("İmza Emlak Asistanı aktif! 🕵️‍♂️");

// Sayfadaki verileri ayıkla (Örnek Sahibinden yapısı)
function scrapeListingData() {
    const data = {
        title: document.title,
        price: document.querySelector('.classifiedInfoValue')?.innerText?.trim() || "Bilinmiyor",
        url: window.location.href,
        timestamp: new Date().toISOString()
    };
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
