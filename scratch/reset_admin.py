import sys
import os

# Add project root to sys.path
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root)

from modules.core.factory import create_app
from shared.extensions import db
from modules.auth.models import User
from modules.auth.service import AuthService

app = create_app()
with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(username='admin').first()
    new_hash = AuthService.hash_password('admin123')
    
    if admin:
        admin.password_hash = new_hash
        admin.is_active = True
        admin.is_admin = True
        admin.role = 'super_admin'
        db.session.commit()
        print("SUCCESS: Admin password reset to admin123.")
    else:
        # Create if missing
        new_admin = User(
            username='admin',
            password_hash=new_hash,
            role='super_admin',
            is_admin=True,
            email='admin@imzaemlak.com',
            email_verified=True
        )
        db.session.add(new_admin)
        db.session.commit()
        print("SUCCESS: Admin user created with password admin123.")
