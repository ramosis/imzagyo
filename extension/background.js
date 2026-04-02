/**
 * Evrensel ROI Asistanı - Background Service Worker
 * Arka planda anonim istatistiklerin gönderimini yönetir.
 */

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "LOG_STATS") {
        sendAnonymousStats(request.data);
        sendResponse({ success: true });
    } else if (request.action === "GET_VALUATION") {
        fetchValuation(request.data).then(sendResponse);
        return true; 
    } else if (request.action === "OPEN_KUTAHYA_EIMAR") {
        warmupKutahya().then(() => {
            chrome.tabs.create({ url: "https://www.kutahya.bel.tr:84/imardurumu/index.aspx" });
        });
        return true;
    }
});

const API_BASE = "http://127.0.0.1:8000";

async function fetchValuation(data) {
    try {
        const response = await fetch(`${API_BASE}/api/v1/valuation/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (e) {
        console.error("Valuation fetch error:", e);
        return { error: "Sunucuya bağlanılamadı" };
    }
}

/**
 * Sadece anonim metrikleri sunucuya gönderir.
 * URL, İlan ID veya Kişisel Veri içermez.
 */
async function sendAnonymousStats(stats) {
    const anonymousData = {
        city: stats.city,
        district: stats.district,
        neighborhood: stats.neighborhood,
        m2: stats.m2,
        price: stats.price,
        timestamp: new Date().toISOString(),
        // Geohash veya benzeri bir anonimleştirme buraya eklenecek
        location_hash: "PLACEHOLDER_HASH" 
    };

    console.log("Sunucuya gönderilen ANONİM veri:", anonymousData);

    try {
        // Not: Gerçek API endpoint'iniz buraya gelecek
        // await fetch('https://api.benimdomainim.com/aggregate', {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(anonymousData)
        // });
    } catch (e) {
        console.error("İstatistik gönderim hatası:", e);
    }
}

async function warmupKutahya() {
    console.log("Kütahya Belediyesi oturum hazırlığı başlatılıyor...");
    try {
        await fetch("https://www.kutahya.bel.tr/", { mode: 'no-cors' });
        console.log("Oturum hazır.");
    } catch (e) {
        console.error("Warmup hatası:", e);
    }
}
