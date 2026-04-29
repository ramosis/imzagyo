try:
    from gevent import monkey
    monkey.patch_all()
except ImportError:
    pass

import sys
import os
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from backend.app.factory import create_app
from backend.app.extensions import socketio

# Uygulama instance'ını yeni Core modülünden oluştur.
app = create_app()

if __name__ == '__main__':
    # Çalışma zamanı ayarlarını çevresel değişkenlerden al
    is_debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 8000))
    
    # Sunucuyu başlat
    socketio.run(app, debug=is_debug, host='0.0.0.0', port=port)
