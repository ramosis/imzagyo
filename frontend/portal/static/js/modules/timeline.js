/**
 * Timeline Module
 * Handles customer portal transaction visualization
 */

export const TimelineModule = {
    async init() {
        console.log("Timeline Module Initializing...");
        await this.loadTransactions();
    },

    async loadTransactions() {
        try {
            const response = await fetch('/api/v1/customer/transactions');
            if (!response.ok) throw new Error("Failed to load transactions");
            
            const transactions = await response.json();
            this.renderTransactions(transactions);
            
            // Load first transaction timeline by default if available
            if (transactions.length > 0) {
                this.loadTimeline(transactions[0].id);
            }
        } catch (error) {
            console.error("Error loading transactions:", error);
        }
    },

    async loadTimeline(transactionId) {
        try {
            const response = await fetch(`/api/v1/customer/transactions/${transactionId}/timeline`);
            const events = await response.json();
            this.renderTimeline(events);
        } catch (error) {
            console.error("Error loading timeline:", error);
        }
    },

    renderTransactions(transactions) {
        const list = document.getElementById('transactions-list');
        if (!list) return;

        list.innerHTML = transactions.map(t => `
            <div class="glass p-4 rounded-2xl border-l-4 border-blue-500 cursor-pointer hover:scale-[1.02] transition-transform" onclick="TimelineModule.loadTimeline(${t.id})">
                <div class="flex justify-between items-start mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-blue-400">${t.type}</span>
                    <span class="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded">${t.status}</span>
                </div>
                <h3 class="font-semibold mb-1">İşlem #${t.id}</h3>
                <p class="text-sm text-slate-400 mb-4">Tarih: ${new Date(t.created_at).toLocaleDateString('tr-TR')}</p>
                <div class="flex justify-between items-center">
                    <span class="font-bold text-lg">₺${t.price.toLocaleString('tr-TR')}</span>
                    <i class="fas fa-chevron-right text-slate-500"></i>
                </div>
            </div>
        `).join('');
    },

    renderTimeline(events) {
        const container = document.querySelector('.relative.pl-12.space-y-12');
        if (!container) return;

        // Keep the vertical line
        container.innerHTML = '<div class="timeline-line"></div>';

        container.innerHTML += events.map(e => `
            <div class="relative">
                <div class="absolute -left-12 mt-1">
                    <div class="milestone-dot ${new Date(e.date) <= new Date() ? 'active-milestone' : 'border-blue-500/50'}">
                        <i class="fas ${this.getIconForType(e.type)} ${new Date(e.date) <= new Date() ? 'text-green-400' : 'text-blue-400'}"></i>
                    </div>
                </div>
                <div>
                    <div class="flex justify-between items-center mb-1">
                        <h4 class="text-lg font-semibold ${new Date(e.date) > new Date() ? 'text-slate-400' : ''}">${e.title}</h4>
                        <span class="text-xs text-slate-500">${new Date(e.date).toLocaleDateString('tr-TR')}</span>
                    </div>
                    <p class="text-slate-400 text-sm">${e.description}</p>
                </div>
            </div>
        `).join('');
    },

    getIconForType(type) {
        const icons = {
            'milestone': 'fa-check',
            'update': 'fa-info-circle',
            'document_added': 'fa-file-alt',
            'appointment': 'fa-calendar-check'
        };
        return icons[type] || 'fa-circle';
    }
};

window.TimelineModule = TimelineModule;
