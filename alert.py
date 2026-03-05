import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

def kirim_alert_login_ilegal(
    email_penerima,
    nama_pengguna,
    ip_address="Tidak diketahui",
    waktu=None,
    jumlah_gagal=1,
    lokasi="Tidak diketahui"
):
    if waktu is None:
        waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")

    token = str(uuid.uuid4())[:12]
    tracking_link = f"{BASE_URL}/track?token={token}&email={email_penerima}"

    subject = "MANDIRI CARE - Peringatan: Percobaan Login Ilegal"

    body = f"""
Halo {nama_pengguna},

Ada percobaan login ilegal ke akun Livin' by Mandiri Anda.

Detail:
- Waktu: {waktu}
- IP: {ip_address}
- Lokasi: {lokasi}
- Jumlah gagal: {jumlah_gagal}

Cek detail sekarang: {tracking_link}

Segera ganti password dan aktifkan 2FA.

Tim Mandiri Care
    """

    msg = MIMEMultipart()
    msg['From'] = f"Mandiri Care <{SENDER_EMAIL}>"
    msg['To'] = email_penerima
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, email_penerima, msg.as_string())
        server.quit()
        print(f"SUKSES kirim ke {email_penerima}")
        return True
    except Exception as e:
        print(f"GAGAL: {e}")
        return False

# Test
if __name__ == "__main__":
    kirim_alert_login_ilegal(
        "kunaepi21@gmail.com",
        "kunaepi.softpren@gmail.com",
        "dwi.softpren@gmail.com",# ganti emailmu
        "Test User",
        ip_address="182.168.1.1",
        jumlah_gagal=4
    )
