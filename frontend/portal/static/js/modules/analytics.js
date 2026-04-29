// --- ANALYTICS / DASHBOARD ---
async function fetchDashboardStats() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/dashboard/stats`) : await fetch(`${base}/dashboard/stats`);
        
        if (res.ok) {
            const stats = await res.json();
            
            const leadsStat = document.getElementById('dash-stat-leads');
            const expensesStat = document.getElementById('dash-stat-expenses');
            
            if (leadsStat) leadsStat.textContent = stats.leads_count || 0;
            if (expensesStat) expensesStat.textContent = stats.pending_expenses_count || 0;
            
            if (typeof fetchPortfoliosForDashboard === 'function') fetchPortfoliosForDashboard();
            if (typeof fetchUpcomingBirthdays === 'function') fetchUpcomingBirthdays();
        }
    } catch (e) {
        console.error('Dashboard Stats error:', e);
    }
}

async function fetchUpcomingBirthdays() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/contacts/birthdays`) : await fetch(`${base}/contacts/birthdays`);
        
        if (res.ok) {
            const birthdays = await res.json();
            const container = document.getElementById('dashboard-birthdays-list');
            if (!container) return; // Null Check
            
            container.innerHTML = birthdays.length === 0 ? '<p class="text-gray-400 text-xs italic">Yaklaşan doğum günü yok.</p>' : '';
            
            birthdays.slice(0, 4).forEach(b => {
                const dayText = b.days_left === 0 ? '<span class="text-red-600 font-bold">BUGÜN!</span>' : `${b.days_left} gün`;
                container.innerHTML += `<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-gold/30 transition-colors">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gold/10 text-gold flex items-center justify-center text-lg"><i class="fa-solid fa-cake-candles"></i></div>
                        <div><p class="text-sm font-bold text-navy">${b.name}</p><p class="text-[10px] text-gray-500">${b.occupation || 'Müşteri'}</p></div>
                    </div>
                    <div class="text-right"><p class="text-xs font-bold text-gold">${dayText}</p></div>
                </div>`;
            });
        }
    } catch (e) {
        console.error('Upcoming Birthdays error:', e);
    }
}
