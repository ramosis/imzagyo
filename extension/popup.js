/**
 * Evrensel ROI Asistanı - Popup Mantığı
 */

let currentData = {
    category: 'Konut',
    listing_type: 'Satılık'
};

document.addEventListener('DOMContentLoaded', async () => {
    // Dil ayarını yükle ve uygula
    const { user_lang = 'tr' } = await chrome.storage.local.get('user_lang');
    const langSelect = document.getElementById('langSelect');
    if (langSelect) langSelect.value = user_lang;
    applyLanguage(user_lang);

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Content script'ten veri iste
>>>>+++ REPLACE

    chrome.tabs.sendMessage(tab.id, { action: "GET_LISTING_DATA" }, (response) => {
        if (chrome.runtime.lastError) {
            console.error("Mesaj gönderme hatası:", chrome.runtime.lastError.message);
            document.getElementById('listingTitle').value = "İletişim hatası. Sayfa script'i aktif mi?";
            updateUI(currentData); // Fallback to default data
            return;
        }
        
        if (response) {
            // Gelen veriyi mevcut veriyle birleştir
            Object.assign(currentData, response);
            updateUI(currentData);
        } else {
            document.getElementById('listingTitle').value = "Veri okunamadı. Sayfayı yenileyin.";
            updateUI(currentData); // Fallback to default data
        }
    });

    // Olay Dinleyicileri
    document.getElementById('rentInput').addEventListener('input', (e) => calculateROI(e.target.value));
    document.getElementById('addToListBtn').addEventListener('click', saveToLocal);
    document.getElementById('openDashboardBtn').addEventListener('click', () => chrome.tabs.create({ url: 'dashboard.html' }));

    // Buton Grubu Dinleyicileri
    document.getElementById('ilan-tipi-group').addEventListener('click', (e) => {
        if (e.target.matches('.option-button')) {
            const value = e.target.dataset.value;
            handleCategoryChange(value);
        }
    });

    document.getElementById('islem-tipi-group').addEventListener('click', (e) => {
        if (e.target.matches('.option-button')) {
            const value = e.target.dataset.value;
            handleListingTypeChange(value);
        }
    });

    // Dil değiştirme
    document.getElementById('langSelect').addEventListener('change', async (e) => {
        const lang = e.target.value;
        await chrome.storage.local.set({ user_lang: lang });
        location.reload(); // Arayüzü tazelemek için en temiz yol
    });
});

function applyLanguage(lang) {
    // i18n anahtarlarına sahip elementleri güncelle
    document.querySelectorAll('[id^="msg-"]').forEach(el => {
        const key = el.id.replace('msg-', '');
        const message = chrome.i18n.getMessage(key);
        if (message) el.innerText = message;
    });

    // Buton metinlerini güncelle
    document.getElementById('addToListBtn').innerText = chrome.i18n.getMessage('addToList');
    document.getElementById('openDashboardBtn').innerText = chrome.i18n.getMessage('openDashboard');
    
    // Placeholderları güncelle
    document.getElementById('rentInput').placeholder = chrome.i18n.getMessage('monthlyRent').replace(' (₺)', '');
    
    // RTL Desteği (Arapça için)
    if (lang === 'ar') {
        document.body.style.direction = 'rtl';
    } else {
        document.body.style.direction = 'ltr';
    }
}
>>>>+++ REPLACE


function handleCategoryChange(value) {
    currentData.category = value;
    
    // Buton aktif durumunu güncelle
    updateButtonGroup('ilan-tipi-group', value);

    // Alanların görünürlüğünü yönet
    const m2Fields = document.getElementById('m2-fields');
    const arsaFields = document.getElementById('arsa-fields');
    const tarlaFields = document.getElementById('tarla-fields');

    // Önce hepsini gizle
    m2Fields.classList.add('hidden');
    arsaFields.classList.add('hidden');
    tarlaFields.classList.add('hidden');

    // Seçime göre göster
    switch(value) {
        case 'Konut':
        case 'Dükkan':
            m2Fields.classList.remove('hidden');
            break;
        case 'Arsa':
            arsaFields.classList.remove('hidden');
            break;
        case 'Tarla':
            tarlaFields.classList.remove('hidden');
            break;
    }
}

function handleListingTypeChange(value) {
    currentData.listing_type = value;
    updateButtonGroup('islem-tipi-group', value);
    // ROI'yi yeniden hesapla çünkü işlem tipi değişti
    calculateROI(document.getElementById('rentInput').value);
}

function updateButtonGroup(groupId, activeValue) {
    const group = document.getElementById(groupId);
    group.querySelectorAll('.option-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.value === activeValue) {
            btn.classList.add('active');
        }
    });
}

function updateUI(data) {
    // Buton gruplarını ayarla
    handleCategoryChange(data.category || 'Konut');
    handleListingTypeChange(data.listing_type || 'Satılık');
    
    // Diğer alanların güncellenmesi
    document.getElementById('listingTitle').value = data.title || '';
    document.getElementById('listingPrice').value = data.price || 'Bilinmiyor';
    document.getElementById('listingM2Brut').value = data.m2_brut || 0;
    document.getElementById('listingM2Net').value = data.m2_net || 0;
    document.getElementById('listingRooms').value = data.rooms || '0+0';
    
    // Değişiklikleri dinle (Override)
    const fields = ['listingTitle', 'listingPrice', 'listingRooms', 'listingM2Brut', 'listingM2Net'];
    fields.forEach(id => {
        document.getElementById(id).addEventListener('input', () => {
            // JS'de bu alanlar için özel bir key-mapping yapmaya gerek yok, saveToLocal'de doğrudan okunuyor.
        });
    });
}

function calculateROI(monthlyRent) {
    const listingType = currentData.listing_type;
    
    // Sadece satılık ilanlarda ROI hesapla
    if (listingType !== 'Satılık') {
        document.getElementById('roiValue').innerText = "N/A";
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
        listing_type: currentData.listing_type, // Değişiklik
        category: currentData.category,       // Değişiklik
        estimated_rent: document.getElementById('rentInput').value,
        url: currentData.url,
        city: currentData.city,
        district: currentData.district,
        neighborhood: currentData.neighborhood,
        saved_at: new Date().toLocaleString()
    };
    
    // Arsa ve Tarla için ek veriler
    if(currentData.category === 'Arsa'){
        itemToSave.emsal = document.getElementById('listingEmsal').value;
        itemToSave.kat_sayisi = document.getElementById('listingKatSayisi').value;
    }
    if(currentData.category === 'Tarla'){
        itemToSave.imara_yakin = document.getElementById('checkImaraYakin').checked;
        itemToSave.gese_uygun = document.getElementById('checkGeseUygun').checked;
    }


    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    my_listings.push(itemToSave);
    
    await chrome.storage.local.set({ my_listings });
    
    const btn = document.getElementById('addToListBtn');
    const originalText = chrome.i18n.getMessage('addToList');
    const addedText = chrome.i18n.getMessage('added');

    btn.innerText = addedText;
    btn.style.background = "#10b981";
    setTimeout(() => {
        btn.innerText = originalText;
        btn.style.background = "#f59e0b";
    }, 2000);
}
>>>>+++ REPLACE

