""" 
İmza Gayrimenkul - WSGI Application Entry Point
Uygulama artık tam App Factory pattern ve modüler Core yapısını kullanıyor. (Phase 28 Unification)
"""
from modules.core.factory import create_app
from shared.extensions import socketio
import os

# Uygulama instance'ını yeni Core modülünden oluştur.
app = create_app()

if __name__ == '__main__':
    # Çalışma zamanı ayarlarını çevresel değişkenlerden al
    is_debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 8000))
    
    # Sunucuyu başlat
    socketio.run(app, debug=is_debug, host='0.0.0.0', port=port)
