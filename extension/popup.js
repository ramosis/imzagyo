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
    // Kategori seçimi - varsayılan değer ayarı
    const categorySelect = document.getElementById('listingCategory');
    categorySelect.value = data.category || 'Daire'; // Varsayılan değer
    
    // İlan tipi seçimi - varsayılan değer ayarı
    const typeSelect = document.getElementById('listingType');
    typeSelect.value = data.listing_type || 'Satılık'; // Varsayılan değer
    
    // Diğer alanların güncellenmesi
    document.getElementById('listingTitle').value = data.title || '';
    document.getElementById('listingPrice').value = data.price || 'Bilinmiyor';
    document.getElementById('listingM2Brut').value = data.m2_brut || 0;
    document.getElementById('listingM2Net').value = data.m2_net || 0;
    document.getElementById('listingRooms').value = data.rooms || '0+0';
    
    // Değişiklikleri dinle (Override)
    const fields = ['listingTitle', 'listingPrice', 'listingRooms', 'listingM2Brut', 'listingM2Net', 'listingType', 'listingCategory'];
    fields.forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            currentData[id.replace('listing', '').toLowerCase()] = document.getElementById(id).value;
            calculateROI(document.getElementById('rentInput').value);
        });
    });
}

function calculateROI(monthlyRent) {
    const listingType = document.getElementById('listingType').value;
    
    // Sadece satılık ilanlarda ROI hesapla
    if (listingType === 'Kiralık') {
        document.getElementById('roiValue').innerText = "REFERANS";
        document.getElementById('roiValue').style.background = "#64748b";
        document.getElementById('amortizationYears').innerText = "-";
        document.getElementById('resultArea').style.display = "block";
        return;
    }

    if (!currentData || !monthlyRent) return;

    const priceRaw = document.getElementById('listingPrice').value;
    const priceNumeric = parseFloat(priceRaw.toString().replace(/\./g, '').replace(/[^\d]/g, ''));
    const rentNumeric = parseFloat(monthlyRent);

    if (priceNumeric > 0 && rentNumeric > 0) {
        const annualRent = rentNumeric * 12;
        const roi = (annualRent / priceNumeric) * 100;
        const amortization = priceNumeric / annualRent;

        document.getElementById('roiValue').innerText = `%${roi.toFixed(2)}`;
        document.getElementById('roiValue').style.background = "#10b981";
        document.getElementById('amortizationYears').innerText = amortization.toFixed(1);
        document.getElementById('resultArea').style.display = "block";

        chrome.runtime.sendMessage({
            action: "LOG_STATS",
            data: {
                city: currentData.city,
                district: currentData.district,
                neighborhood: currentData.neighborhood,
                m2: document.getElementById('listingM2Brut').value,
                price: priceNumeric
            }
        });
    }
}

async function saveToLocal() {
    if (!currentData) return;

    const itemToSave = {
        title: document.getElementById('listingTitle').value,
        price: document.getElementById('listingPrice').value,
        rooms: document.getElementById('listingRooms').value,
        m2_brut: document.getElementById('listingM2Brut').value,
        m2_net: document.getElementById('listingM2Net').value,
        listing_type: document.getElementById('listingType').value,
        category: document.getElementById('listingCategory').value,
        estimated_rent: document.getElementById('rentInput').value,
        url: currentData.url,
        city: currentData.city,
        district: currentData.district,
        neighborhood: currentData.neighborhood,
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
