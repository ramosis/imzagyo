from modules.core.factory import create_app
from shared.extensions import db
from modules.auth.repository import UserRepository
from shared.models import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
    for u in users:
        print(f"ID: {u.id}, Username: {u.username}, Role: {u.role}, Active: {u.is_active}")
