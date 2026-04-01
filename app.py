""" 
İmza Gayrimenkul - Main Application Entry Point
Uygulama artık tam App Factory pattern kullanıyor.
"""
from app.factory import create_app
from shared.extensions import socketio
import os

# Uygulama instance'ını oluştur (load_dotenv içeride çalışır)
app = create_app()

if __name__ == '__main__':
    # Çalışma zamanı ayarlarını çevresel değişkenlerden al
    is_debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 8000))
    
    # Sunucuyu başlat
    socketio.run(app, debug=is_debug, host='0.0.0.0', port=port)
