// --- AI MODULE ---
async function generateStoryFromAI() {
    const btn = document.getElementById('btn-ai-generate');
    if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Yazılıyor...';
    
    // Null Checks for inputs
    const priceEl = document.getElementById('p-fiyat');
    const locEl = document.getElementById('p-lokasyon');
    const roomEl = document.getElementById('p-oda');
    const typeEl = document.getElementById('p-alt_tip');
    const featEl = document.getElementById('p-ozellikler_arr');
    const storyEl = document.getElementById('p-hikaye');
    
    if (!priceEl || !locEl || !roomEl || !typeEl || !featEl || !storyEl) {
        console.warn('AI form elements missing');
        if (btn) btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> AI ile Üret';
        return;
    }

    const payload = {
        fiyat: priceEl.value,
        il_ilce: locEl.value,
        oda: roomEl.value,
        alt_tip: typeEl.value,
        ozellikler: featEl.value
    };
    
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' 
            ? await apiFetch(`${base}/generate-summary`, { method: 'POST', body: JSON.stringify(payload) }) 
            : await fetch(`${base}/generate-summary`, { method: 'POST', body: JSON.stringify(payload), headers: { 'Content-Type': 'application/json' } });
            
        const data = await res.json();
        if (res.ok && data.story) {
            storyEl.value = data.story;
            if (typeof showToast === 'function') showToast('Yapay zeka özeti başarıyla oluşturuldu.', 'success');
        } else {
            alert('Yapay zeka hatası: ' + (data.error || 'Bilinmeyen hata'));
        }
    } catch (err) {
        console.error('AI Generate error:', err);
    } finally {
        if (btn) btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> AI ile Üret';
    }
}
