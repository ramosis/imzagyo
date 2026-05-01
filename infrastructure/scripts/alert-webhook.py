#!/usr/bin/env python3
import json
import os
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

SLACK_WEBHOOK = os.getenv('SLACK_WEBHOOK_URL')

class AlertHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        print(f"Received alert: {json.dumps(data)}")
        
        for alert in data.get('alerts', []):
            self.send_to_slack(alert)
        
        self.send_response(200)
        self.end_headers()
    
    def send_to_slack(self, alert):
        status = alert.get('status')
        annotations = alert.get('annotations', {})
        labels = alert.get('labels', {})
        
        color = "#ff0000" if status == "firing" else "#00ff00"
        title = f"{'🚨' if status == 'firing' else '✅'} {annotations.get('summary', 'Alert')}"
        
        payload = {
            "attachments": [{
                "fallback": title,
                "color": color,
                "title": title,
                "text": annotations.get('description', 'No description'),
                "fields": [
                    {"title": "Severity", "value": labels.get('severity', 'N/A'), "short": True},
                    {"title": "Status", "value": status.upper(), "short": True}
                ]
            }]
        }
        
        if SLACK_WEBHOOK:
            try:
                requests.post(SLACK_WEBHOOK, json=payload)
            except Exception as e:
                print(f"Failed to send Slack alert: {e}")
        else:
            print("SLACK_WEBHOOK_URL not set. Skipping Slack notification.")

if __name__ == '__main__':
    port = 9094
    server = HTTPServer(('0.0.0.0', port), AlertHandler)
    print(f"Alert Webhook listening on port {port}...")
    server.serve_forever()
