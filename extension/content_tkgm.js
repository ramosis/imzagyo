/**
 * Real Estate Pro - TKGM Parsel Sorgu Content Script
 */

console.log("Parsel Sorgu Asistanı Aktif 🌐");

// Attribute panelini izleyen MutationObserver
const observer = new MutationObserver((mutations) => {
    const attributePanel = document.querySelector('.attribute-content');
    if (attributePanel && !document.getElementById('save-parsel-btn')) {
        injectSaveButton(attributePanel);
    }
});

observer.observe(document.body, { childList: true, subtree: true });

/**
 * Kaydet butonunu attribute paneline enjekte eder.
 */
function injectSaveButton(container) {
    const btn = document.createElement('button');
    btn.id = 'save-parsel-btn';
    btn.innerText = '📌 Parseli Projeye Kaydet';
    btn.style.cssText = `
        background-color: #c5a059;
        color: white;
        border: none;
        padding: 10px;
        width: 100%;
        margin-top: 10px;
        cursor: pointer;
        font-weight: bold;
        border-radius: 4px;
    `;

    btn.onclick = () => saveCurrentParsel();
    container.appendChild(btn);
}

/**
 * Mevcut parsel verilerini toplar ve kaydeder.
 */
function saveCurrentParsel() {
    const rows = Array.from(document.querySelectorAll('.attribute-content table tr'));
    const info = {};

    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 2) {
            const label = cells[0].innerText.trim();
            const value = cells[1].innerText.trim();
            info[label] = value;
        }
    });

    // Veriyi standardize et
    const parselData = {
        id: Date.now(),
        il: info["İl"] || "",
        ilce: info["İlçe"] || "",
        mahalle: info["Mahalle"] || "",
        ada: info["Ada"] || "",
        parsel: info["Parsel"] || "",
        alan: info["Alan"] || info["Yüzölçümü"] || "",
        nitelik: info["Nitelik"] || "",
        mevki: info["Mevkii"] || "",
        timestamp: new Date().toLocaleString()
    };

    chrome.storage.local.get({ savedParcels: [] }, (result) => {
        const parcels = result.savedParcels;
        // Mükerrer kaydı önle
        const exists = parcels.find(p => p.ada === parselData.ada && p.parsel === parselData.parsel && p.mahalle === parselData.mahalle);
        
        if (!exists) {
            parcels.push(parselData);
            chrome.storage.local.set({ savedParcels: parcels }, () => {
                alert(`✅ ${parselData.ada}/${parselData.parsel} başarıyla kaydedildi!`);
            });
        } else {
            alert("⚠️ Bu parsel zaten kayıtlı.");
        }
    });
}
