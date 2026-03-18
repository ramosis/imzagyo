/**
 * Evrensel ROI Asistanı - Background Service Worker
 * Arka planda anonim istatistiklerin gönderimini yönetir.
 */

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "LOG_STATS") {
        sendAnonymousStats(request.data);
        sendResponse({ success: true });
    }
});

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
