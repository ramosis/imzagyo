import { apiFetch } from '../core/api.js';
import { showToast } from '../core/ui.js';

export async function fetchContracts() {
    try {
        // Updated URL as per Phase 4D.2
        const res = await apiFetch('finance/contracts');
        if (!res.ok) throw new Error('Sözleşmeler yüklenemedi');
        
        const data = await res.json();
        renderContracts(data);
    } catch (err) {
        console.error('[Finance] Hata:', err);
        showToast('Sözleşmeler yüklenirken hata oluştu', 'error');
    }
}

function renderContracts(data) {
    const tableBody = document.getElementById('contracts-table-body');
    if (!tableBody) return;

    tableBody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="text-center py-8 text-gray-400">Sözleşme bulunamadı.</td></tr>' : '';
    data.forEach(c => {
        tableBody.innerHTML += `
            <tr class="border-b border-gray-100 hover:bg-gray-50/50 transition-colors group">
                <td class="py-4 px-6 font-bold text-navy">${c.contract_no || '-'}</td>
                <td class="py-4 px-6 text-sm text-gray-600">${c.client_name || '-'}</td>
                <td class="py-4 px-6">
                    <span class="px-2 py-1 rounded text-[10px] font-bold uppercase ${c.status === 'active' ? 'bg-emerald-100 text-emerald-700' : 'bg-gray-100 text-gray-600'}">
                        ${c.status || 'Taslak'}
                    </span>
                </td>
                <td class="py-4 px-6 font-bold text-slate-700">${c.amount || '-'}</td>
                <td class="py-4 px-6 text-right">
                    <button class="view-contract-btn text-navy hover:text-gold" data-id="${c.id}"><i class="fa-solid fa-file-invoice"></i> Detay</button>
                </td>
            </tr>`;
    });
}

export async function fetchPayroll() {
    try {
        const res = await apiFetch('finance/payroll');
        if (!res.ok) throw new Error('Hakedişler yüklenemedi');
        const data = await res.json();
        renderPayroll(data);
    } catch (err) { console.error(err); }
}

function renderPayroll(data) {
    const tableBody = document.getElementById('payroll-table-body');
    if (!tableBody) return;
    // ... render logic
}

// Auto-init
window.addEventListener('sectionShown', (e) => {
    if (e.detail.sectionId === 'contracts') fetchContracts();
    if (e.detail.sectionId === 'payroll') fetchPayroll();
    if (e.detail.sectionId === 'finance') {
        // Load general finance dashboard stats if needed
    }
});
