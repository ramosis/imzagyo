/**
 * Real Estate Pro - Kütahya Belediyesi E-İmar Content Script
 */

console.log("Kütahya E-İmar Asistanı Aktif 🏗️");

// Popup'tan gelen veriyi bekle ve formları doldur
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "FILL_E_IMAR_FORM") {
        fillForm(request.data);
    }
});

/**
 * Ada/Parsel/Mahalle bilgilerini KEOS formuna doldurur.
 */
function fillForm(data) {
    console.log("Form dolduruluyor:", data);

    // Kütahya Belediyesi (Netcad KEOS) Seçicileri
    // Not: Bu seçiciler frame içinde olabilir, kontrol edilmeli.
    const mahalleSelect = document.querySelector('select[id*="ddlMahalle"]');
    const adaInput = document.querySelector('input[id*="txtAda"]');
    const parselInput = document.querySelector('input[id*="txtParsel"]');
    const searchBtn = document.querySelector('input[id*="btnSorgula"]');

    if (mahalleSelect && data.mahalle) {
        // Mahalle seçimi (Text eşleşmesiyle)
        for (let i = 0; i < mahalleSelect.options.length; i++) {
            if (mahalleSelect.options[i].text.includes(data.mahalle.toUpperCase())) {
                mahalleSelect.selectedIndex = i;
                mahalleSelect.dispatchEvent(new Event('change'));
                break;
            }
        }
    }

    if (adaInput) adaInput.value = data.ada;
    if (parselInput) parselInput.value = data.parsel;

    if (searchBtn) {
        // searchBtn.click(); // Otomatik tıklama opsiyonel
        console.log("Veriler dolduruldu, sorgulama yapılabilir.");
    }
}
