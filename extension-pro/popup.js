/**
 * Real Estate Pro - Popup UI Controller
 */

document.addEventListener('DOMContentLoaded', () => {
    loadSavedParcels();
});

function loadSavedParcels() {
    const listContainer = document.getElementById('parcel-list');
    
    chrome.storage.local.get({ savedParcels: [] }, (result) => {
        const parcels = result.savedParcels;

        if (parcels.length === 0) {
            listContainer.innerHTML = '<div class="empty-state">Henüz kaydedilmiş parsel yok.<br/><small>Parsel Sorgu sitesinden seçim yapıp kaydedin.</small></div>';
            return;
        }

        listContainer.innerHTML = '';
        parcels.reverse().forEach((p, index) => {
            const card = document.createElement('div');
            card.className = 'parcel-card';
            card.innerHTML = `
                <div class="parcel-header">
                    <span>Ada/Parsel: ${p.ada}/${p.parsel}</span>
                    <button class="delete-btn" data-index="${index}">[SİL]</button>
                </div>
                <div class="parcel-details">
                    ${p.il} / ${p.ilce} / ${p.mahalle}<br/>
                    Alan: ${p.alan} | Nitelik: ${p.nitelik}<br/>
                    <em>Kayıt: ${p.timestamp}</em>
                </div>
                <div class="actions">
                    <button class="btn-tkgm" data-id="${p.id}">📍 TKGM'de Aç</button>
                    <button class="btn-imar" data-id="${p.id}">🏗️ E-İmar (Kütahya)</button>
                </div>
            `;
            listContainer.appendChild(card);
        });

        // Event Listeners
        document.querySelectorAll('.btn-imar').forEach(btn => {
            btn.onclick = (e) => openEImar(e.target.dataset.id);
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.onclick = (e) => deleteParcel(e.target.dataset.index);
        });
    });
}

function openEImar(id) {
    chrome.storage.local.get({ savedParcels: [] }, (result) => {
        const parcel = result.savedParcels.find(p => p.id == id);
        if (parcel) {
            // Background script'e mesaj gönder (Isınma + Açma)
            chrome.runtime.sendMessage({ 
                action: "OPEN_KUTAHYA_EIMAR", 
                data: parcel 
            });
            
            // content_kutahya'ya veriyi göndermek için biraz bekleyelim (sayfa yüklenince)
            // Not: content_kutahya sayfa yüklenince mesaj bekliyor.
            // Ama background tab'ı yeni açtığı için mesajı o anda yakalayamaz. 
        }
    });
}

function deleteParcel(index) {
    chrome.storage.local.get({ savedParcels: [] }, (result) => {
        const parcels = result.savedParcels.reverse(); // Reverse'li haliyle index eşleşmeli
        parcels.splice(index, 1);
        chrome.storage.local.set({ savedParcels: parcels.reverse() }, () => {
            loadSavedParcels();
        });
    });
}
