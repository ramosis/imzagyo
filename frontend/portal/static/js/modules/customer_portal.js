/**
 * Imza Gayrimenkul - Customer Portal Module (Phase 9)
 * Manages transaction timeline and document transparency.
 */

export const customer_portal = {
    init: async () => {
        console.log("Customer Portal module initialized");
        await customer_portal.loadDashboardData();
    },

    loadDashboardData: async () => {
        try {
            // 1. İşlemleri getir
            const response = await fetch('/api/v1/customer/transactions');
            const transactions = await response.json();

            if (transactions.length === 0) {
                document.getElementById('transaction-timeline').innerHTML = '<p class="empty-state">Henüz aktif bir işleminiz bulunmamaktadır.</p>';
                return;
            }

            // Şimdilik ilk (en güncel) işlemi baz alıyoruz
            const activeTransaction = transactions[0];
            customer_portal.updateSummary(activeTransaction);
            
            // 2. Timeline'ı getir
            await customer_portal.loadTimeline(activeTransaction.id);
            
            // 3. Dökümanları getir
            await customer_portal.loadDocuments(activeTransaction.id);

        } catch (error) {
            console.error("Dashboard verisi yüklenirken hata:", error);
        }
    },

    updateSummary: (transaction) => {
        document.getElementById('property-title').textContent = transaction.type === 'sale' ? 'Satış İşlemi' : 'Kiralama İşlemi';
        document.getElementById('process-status').textContent = transaction.status.toUpperCase();
        document.getElementById('last-update').textContent = new Date(transaction.created_at).toLocaleDateString('tr-TR');
        
        // Örnek danışman verisi (Normalde API'den gelmeli)
        document.getElementById('agent-name').textContent = "Mehmet Yılmaz";
    },

    loadTimeline: async (transactionId) => {
        const container = document.getElementById('transaction-timeline');
        try {
            const response = await fetch(`/api/v1/customer/transactions/${transactionId}/timeline`);
            const events = await response.json();

            if (events.length === 0) {
                container.innerHTML = '<p>Zaman çizelgesi henüz oluşturulmadı.</p>';
                return;
            }

            container.innerHTML = events.map(event => `
                <div class="timeline-item">
                    <div class="timeline-icon">
                        <i class="fas ${event.icon || 'fa-circle'}"></i>
                    </div>
                    <div class="timeline-content">
                        <span class="date">${new Date(event.date).toLocaleDateString('tr-TR')}</span>
                        <h3>${event.title}</h3>
                        <p>${event.description}</p>
                    </div>
                </div>
            `).join('');

            // Tamamlanma oranını hesapla (Örnek: toplam event sayısına göre)
            const rate = Math.min(Math.round((events.length / 5) * 100), 100);
            document.getElementById('completion-rate').textContent = `%${rate} Tamamlandı`;

        } catch (error) {
            container.innerHTML = '<p>Timeline yüklenemedi.</p>';
        }
    },

    loadDocuments: async (transactionId) => {
        const list = document.getElementById('document-list');
        try {
            const response = await fetch(`/api/v1/customer/transactions/${transactionId}/documents`);
            const docs = await response.json();

            if (docs.length === 0) {
                list.innerHTML = '<p class="empty-state">Henüz paylaşılan döküman yok.</p>';
                return;
            }

            list.innerHTML = docs.map(doc => `
                <li class="document-item" onclick="window.open('${doc.url}', '_blank')">
                    <div class="file-icon">
                        <i class="fas ${customer_portal.getFileIcon(doc.type)}"></i>
                    </div>
                    <div class="file-info">
                        <span class="file-name">${doc.title}</span>
                        <span class="file-meta">${doc.size || 'Bilinmiyor'} • ${doc.category || 'Genel'}</span>
                    </div>
                    <div class="download-btn">
                        <i class="fas fa-download"></i>
                    </div>
                </li>
            `).join('');

        } catch (error) {
            list.innerHTML = '<p>Dökümanlar yüklenemedi.</p>';
        }
    },

    getFileIcon: (type) => {
        const icons = {
            'pdf': 'fa-file-pdf',
            'doc': 'fa-file-word',
            'docx': 'fa-file-word',
            'jpg': 'fa-file-image',
            'png': 'fa-file-image'
        };
        return icons[type] || 'fa-file-alt';
    },

    contactAgent: () => {
        const phone = "905551234567"; // Örnek
        const message = "Merhaba, işlem sürecim hakkında bir sorum olacaktı.";
        window.open(`https://wa.me/${phone}?text=${encodeURIComponent(message)}`, '_blank');
    }
};
