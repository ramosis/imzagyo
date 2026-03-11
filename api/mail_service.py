import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# E-posta Ayarları (Varsayılanlar .env'den alınmalıdır)
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))
SMTP_USER = os.environ.get("SMTP_USER", "info@imzagayrimenkul.com")
SMTP_PASS = os.environ.get("SMTP_PASS", "your-app-password-here")
MAIL_FROM = os.environ.get("MAIL_FROM", "İmza Gayrimenkul <info@imzagayrimenkul.com>")

def send_email(subject, recipient, body_html):
    """
    Belirtilen alıcıya HTML formatında e-posta gönderir.
    """
    try:
        msg = MIMEMultipart()
        msg['From'] = MAIL_FROM
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(body_html, 'html'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        return True, "E-posta başarıyla gönderildi."
    except Exception as e:
        print(f"E-posta gönderme hatası: {str(e)}")
        return False, str(e)

def send_password_reset_email(email, token, username):
    """
    Şifre sıfırlama e-postası şablonunu hazırlar ve gönderir.
    """
    reset_url = f"https://imzagayrimenkul.com/reset-password?token={token}"
    
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 10px;">
        <h2 style="color: #D4AF37; text-align: center;">İmza Gayrimenkul</h2>
        <p>Merhaba <strong>{username}</strong>,</p>
        <p>Hesabınız için bir şifre sıfırlama talebi aldık. Şifrenizi sıfırlamak için aşağıdaki butona tıklayabilirsiniz:</p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{reset_url}" style="background-color: #D4AF37; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">Şifremi Sıfırla</a>
        </div>
        <p>Eğer bu talebi siz yapmadıysanız, bu e-postayı görmezden gelebilirsiniz. Şifreniz değişmeyecektir.</p>
        <hr style="border: 0; border-top: 1px solid #eeeeee; margin: 20px 0;">
        <p style="font-size: 12px; color: #777777; text-align: center;">
            Bu otomatik bir e-postadır, lütfen yanıtlamayınız.<br>
            &copy; 2026 İmza Gayrimenkul & Yatırım
        </p>
    </div>
    """
    return send_email("Şifre Sıfırlama Talebi - İmza Gayrimenkul", email, html)
