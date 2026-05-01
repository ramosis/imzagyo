import { apiFetch } from '../core/api.js';
import { showToast } from '../core/ui.js';

export async function generateSummary(payload) {
    try {
        const res = await apiFetch('ai/generate-summary', {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        
        if (!res.ok) throw new Error('AI özeti oluşturulamadı');
        return await res.json();
    } catch (err) {
        console.error('[AI] Hata:', err);
        showToast('Yapay zeka yanıt vermiyor', 'warning');
        return null;
    }
}

export async function askGemini(query, context = {}) {
    try {
        const res = await apiFetch('ai/ask', {
            method: 'POST',
            body: JSON.stringify({ query, context })
        });
        
        if (!res.ok) throw new Error('AI yanıtı alınamadı');
        return await res.json();
    } catch (err) {
        console.error('[AI] Hata:', err);
        showToast('AI bağlantı hatası', 'error');
        return null;
    }
}

export async function fetchAiReports() {
    try {
        const res = await apiFetch('ai/reports');
        if (res.ok) {
            const data = await res.json();
            renderAiReports(data);
        }
    } catch (err) { console.error(err); }
}

function renderAiReports(data) {
    const container = document.getElementById('ai-reports-container');
    if (!container) return;
    // ... render logic
}

// Auto-init
window.addEventListener('sectionShown', (e) => {
    if (e.detail.sectionId === 'ai-reports') fetchAiReports();
});
