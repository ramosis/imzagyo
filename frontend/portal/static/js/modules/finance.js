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

// Stubs for future implementation based on the portal logic
async function fetchExpenses() {
    console.log('Fetching expenses...');
}

async function fetchContracts() {
    console.log('Fetching contracts...');
}

async function fetchTaxes() {
    console.log('Fetching taxes...');
}

async function fetchPayroll() {
    console.log('Fetching payroll...');
}