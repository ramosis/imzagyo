/**
 * İmza GYO - Market Analytics Engine
 * Pazar trendlerini ve ROI analizlerini görselleştirir.
 */

let priceTrendChart = null;
let neighborhoodChart = null;

async function updateAnalytics() {
    const region = document.getElementById('analytics-region').value;
    console.log(`Updating analytics for region: ${region}`);
    
    try {
        const response = await fetch(`/api/v1/analytics/market?region=${region}`);
        const data = await response.json();
        
        // Stat güncelleme
        document.getElementById('stat-avg-price').innerText = `₺${data.stats.avg_price.toLocaleString('tr-TR')}`;
        document.getElementById('stat-market-supply').innerText = data.stats.market_supply;
        document.getElementById('stat-avg-roi').innerText = `${data.stats.avg_roi} Yıl`;
        
        // Grafikleri çiz
        renderPriceTrendChart(data.charts.priceTrend);
        renderNeighborhoodChart(data.charts.neighborhoods);
        
    } catch (error) {
        console.error("Analytics Error:", error);
    }
}

function renderPriceTrendChart(chartData) {
    const ctx = document.getElementById('priceTrendChart').getContext('2d');
    
    if (priceTrendChart) priceTrendChart.destroy();
    
    priceTrendChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'Ortalama m² Fiyatı',
                data: chartData.values,
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                fill: true,
                tension: 0.4,
                borderWidth: 3,
                pointRadius: 4,
                pointBackgroundColor: '#fff',
                pointBorderColor: '#6366f1'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

function renderNeighborhoodChart(chartData) {
    const ctx = document.getElementById('neighborhoodChart').getContext('2d');
    
    if (neighborhoodChart) neighborhoodChart.destroy();
    
    neighborhoodChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: chartData.labels,
            datasets: [{
                label: 'İlan Sayısı',
                data: chartData.values,
                backgroundColor: ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'],
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(0,0,0,0.05)' }
                },
                x: {
                    grid: { display: false }
                }
            }
        }
    });
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    // Chart.js kütüphanesini kontrol et, yoksa yükle (veya portal.html'e eklenir)
    if (typeof Chart === 'undefined') {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
        script.onload = updateAnalytics;
        document.head.appendChild(script);
    } else {
        updateAnalytics();
    }
});
