/**
 * Evrensel ROI Asistanı - Popup Mantığı
 */

let currentData = null;

document.addEventListener('DOMContentLoaded', async () => {
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Content script'ten veri iste
    chrome.tabs.sendMessage(tab.id, { action: "GET_LISTING_DATA" }, (response) => {
        if (response) {
            currentData = response;
            updateUI(response);
        } else {
            document.getElementById('listingTitle').innerText = "Veri okunamadı. Sayfayı yenileyin.";
        }
    });

    // Kira girişi dinleyici
    document.getElementById('rentInput').addEventListener('input', (e) => {
        calculateROI(e.target.value);
    });

    // Listeye Ekle butonu
    document.getElementById('addToListBtn').addEventListener('click', saveToLocal);

    // Paneli Aç butonu
    document.getElementById('openDashboardBtn').addEventListener('click', () => {
        chrome.tabs.create({ url: 'dashboard.html' });
    });
});

function updateUI(data) {
    document.getElementById('listingTitle').innerText = data.title;
    document.getElementById('listingPrice').innerText = data.price;
    document.getElementById('listingM2').innerText = data.m2;
}

function calculateROI(monthlyRent) {
    if (!currentData || !monthlyRent) return;

    // Fiyattan sayısal değeri ayıkla (Örn: "1.250.000 TL" -> 1250000)
    const priceNumeric = parseFloat(currentData.price.toString().replace(/\./g, '').replace(/[^\d]/g, ''));
    const rentNumeric = parseFloat(monthlyRent);

    if (priceNumeric > 0 && rentNumeric > 0) {
        const annualRent = rentNumeric * 12;
        const roi = (annualRent / priceNumeric) * 100;
        const amortization = priceNumeric / annualRent;

        document.getElementById('roiValue').innerText = `%${roi.toFixed(2)}`;
        document.getElementById('amortizationYears').innerText = amortization.toFixed(1);
        document.getElementById('resultArea').style.display = "block";

        // Anonim istatistik gönder (Background arkada halleder)
        chrome.runtime.sendMessage({
            action: "LOG_STATS",
            data: {
                city: currentData.city,
                district: currentData.district,
                neighborhood: currentData.neighborhood,
                m2: currentData.m2,
                price: priceNumeric
            }
        });
    }
}

async function saveToLocal() {
    if (!currentData) return;

    const rent = document.getElementById('rentInput').value;
    const itemToSave = {
        ...currentData,
        estimated_rent: rent,
        saved_at: new Date().toLocaleString()
    };

    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    my_listings.push(itemToSave);
    
    await chrome.storage.local.set({ my_listings });
    
    const btn = document.getElementById('addToListBtn');
    btn.innerText = "✅ Eklendi!";
    btn.style.background = "#10b981";
    setTimeout(() => {
        btn.innerText = "🌟 Karşılaştırma Listeme Ekle";
        btn.style.background = "#f59e0b";
    }, 2000);
}
