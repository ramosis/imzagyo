import os

def send_password_reset_email(email, token, username):
    """Mock mail service for now."""
    print(f"Sending password reset email to {email} for user {username} with token {token}")
    # Actual implementation with Flask-Mail or SMTP would go here
    return True
