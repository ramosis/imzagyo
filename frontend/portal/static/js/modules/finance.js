// --- EXPENSES & FINANCE ---
async function approveExpense(id) {
    if (!confirm('Harcamayı onaylamak istiyor musunuz?')) return;
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/expenses/${id}/approve`, { method: 'PUT' }) : await fetch(`${base}/expenses/${id}/approve`, { method: 'PUT' });
        
        if (res.ok) {
            if (typeof fetchExpenses === 'function') fetchExpenses();
            if (typeof showToast === 'function') showToast('Harcama onaylandı', 'success');
        } else {
            if (typeof showToast === 'function') showToast('Harcama onaylanamadı', 'error');
        }
    } catch (e) {
        console.error('Approve Expense error:', e);
    }
}

async function fetchExpenses() {
    console.log('Fetching expenses...');
}

async function fetchContracts() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        // YENİ (Aşama 2'de taşınan endpoint)
        return typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/finance/contracts/`) : await fetch(`${base}/finance/contracts/`);
    } catch (err) {
        console.error('Fetch Contracts error:', err);
    }
}

async function fetchTaxes() {
    console.log('Fetching taxes...');
}

async function fetchPayroll() {
    console.log('Fetching payroll...');
}