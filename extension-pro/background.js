/**
 * Real Estate Pro - Background Service Worker
 */

// Kütahya Belediyesi yönlendirme sorunu için "Warm-up" (Isınma) fonksiyonu
async function warmupKutahya() {
    console.log("Kütahya Belediyesi oturum hazırlığı başlatılıyor...");
    try {
        await fetch("https://www.kutahya.bel.tr/", { mode: 'no-cors' });
        console.log("Oturum hazır.");
    } catch (e) {
        console.error("Warmup hatası:", e);
    }
}

// E-imar sayfasını açmadan önce hazırlık yap
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "OPEN_KUTAHYA_EIMAR") {
        warmupKutahya().then(() => {
            chrome.tabs.create({ url: "https://www.kutahya.bel.tr:84/imardurumu/index.aspx" });
        });
    }
});
