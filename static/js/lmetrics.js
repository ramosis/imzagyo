/**
 * L-Metrics: İmza Gayrimenkul Davranış Analitiği Kütüphanesi
 * Bu kütüphane sadece öz-site üzerinde çalışır ve anonim davranış verisi toplar.
 */

(function() {
    const CONFIG = {
        endpoint: '/api/lmetrics/collect',
        stayInterval: 30000, // 30 saniyede bir "kalma" verisi gönder
        scrollThresholds: [25, 50, 75, 100]
    };

    let sessionID = localStorage.getItem('imza_lmetrics_session') || 
                   'sess_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('imza_lmetrics_session', sessionID);

    let sentScrollThresholds = [];
    let lastStaySent = Date.now();

    function sendData(event_type, element_id = null, value = null) {
        const payload = {
            session_id: sessionID,
            url: window.location.href,
            event_type: event_type,
            element_id: element_id,
            value: value ? value.toString() : null
        };

        fetch(CONFIG.endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        }).catch(err => console.error('L-Metrics Error:', err));
    }

    // 1. Scroll Takibi
    window.addEventListener('scroll', () => {
        const h = document.documentElement, 
              b = document.body,
              st = 'scrollTop',
              sh = 'scrollHeight';
        const percent = (h[st]||b[st]) / ((h[sh]||b[sh]) - h.clientHeight) * 100;

        CONFIG.scrollThresholds.forEach(threshold => {
            if (percent >= threshold && !sentScrollThresholds.includes(threshold)) {
                sendData('scroll', null, threshold);
                sentScrollThresholds.push(threshold);
            }
        });
    });

    // 2. Click Takibi (Otomatik data-lmetrics-id olanlar)
    document.addEventListener('click', (e) => {
        const target = e.target.closest('[data-lmetrics-id]');
        if (target) {
            sendData('click', target.getAttribute('data-lmetrics-id'), target.innerText);
        }
    });

    // 3. Focus / Visibility Takibi
    document.addEventListener('visibilitychange', () => {
        sendData('focus', null, document.visibilityState);
    });

    // 4. Stay (Süre) Takibi
    setInterval(() => {
        if (document.visibilityState === 'visible') {
            const now = Date.now();
            if (now - lastStaySent >= CONFIG.stayInterval) {
                sendData('stay', null, Math.floor((now - lastStaySent) / 1000));
                lastStaySent = now;
            }
        }
    }, 10000);

    // Initial load
    sendData('pageview');
    console.log('L-Metrics Initialized: ' + sessionID);
})();
