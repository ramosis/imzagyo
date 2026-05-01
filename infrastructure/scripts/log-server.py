#!/usr/bin/env python3
import json
import os
from datetime import datetime, timedelta
from collections import deque
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Son 10,000 log satırını bellekte tutan buffer
LOG_BUFFER = deque(maxlen=10000)

@app.route('/ingest', methods=['POST'])
def ingest():
    logs = request.get_json() or []
    if isinstance(logs, dict): logs = [logs]
    
    for log in logs:
        log['_received'] = datetime.utcnow().isoformat()
        LOG_BUFFER.append(log)
    return jsonify({'ingested': len(logs)})

@app.route('/query', methods=['GET'])
def query():
    q = request.args.get('q', '')
    limit = int(request.args.get('limit', 100))
    
    results = []
    for log in reversed(LOG_BUFFER):
        if q and q not in str(log):
            continue
        results.append(log)
        if len(results) >= limit:
            break
    
    return jsonify({'results': results, 'total': len(LOG_BUFFER)})

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, count=len(LOG_BUFFER))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>İmza Gayrimenkul - Hafif Log Paneli</title>
    <style>
        body { font-family: monospace; background: #1a1a2e; color: #a78bfa; padding: 20px; }
        .log-entry { border-bottom: 1px solid #2d1f4e; padding: 5px 0; font-size: 12px; }
        input { background: #0f172a; border: 1px solid #4ade80; color: #fff; padding: 5px; width: 300px; }
        button { background: #4ade80; border: none; padding: 5px 15px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🚀 Hafif Log Sunucusu ({{ count }} kayıt)</h1>
    <form method="GET">
        <input name="q" placeholder="Loglarda ara..." value="{{ request.args.get('q', '') }}">
        <button type="submit">Filtrele</button>
    </form>
    <div id="logs-container" style="margin-top: 20px;">
        {% for log in logs %}
            <div class="log-entry">{{ log }}</div>
        {% endfor %}
    </div>
    <script>
        // Opsiyonel: Auto-refresh veya AJAX query eklenebilir
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
