""" 
Main Application Entry Point
Uses the Application Factory pattern to initialize the Flask app.
"""
import os
from dotenv import load_dotenv
from app.factory import create_app
from shared.extensions import socketio

# Load environment variables
load_dotenv()

# Create application instance
app = create_app()

if __name__ == '__main__':
    # Flask sunucusunu başlat (Docker için 0.0.0.0'a bağlamak şart)
    is_debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    socketio.run(app, debug=is_debug, host='0.0.0.0', port=8000)
