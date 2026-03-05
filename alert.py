import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid
import time  # tambah delay biar tidak kena rate limit Gmail

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
    """.strip()

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
        print(f"GAGAL ke {email_penerima}: {e}")
        return False

# Fungsi baru untuk kirim ke banyak email
def kirim_alert_ke_banyak(
    daftar_penerima,  # list of tuples: [(email1, nama1), (email2, nama2), ...]
    ip_address="Tidak diketahui",
    jumlah_gagal=1,
    lokasi="Tidak diketahui"
):
    sukses_count = 0
    for email, nama in daftar_penerima:
        if kirim_alert_login_ilegal(
            email_penerima=email,
            nama_pengguna=nama,
            ip_address=ip_address,
            jumlah_gagal=jumlah_gagal,
            lokasi=lokasi
        ):
            sukses_count += 1
        time.sleep(1)  # delay 1 detik antar kirim (hindari blok Gmail)

    print(f"\nSelesai! Sukses: {sukses_count}/{len(daftar_penerima)}")

# Test kirim ke banyak
if __name__ == "__main__":
    # Contoh daftar penerima (ganti dengan list real-mu, bisa dari CSV/DB)
    penerima_list = [
        ("kunaepi21@gmail.com", "Kunaepi"),
        ("dwi.softpren@gmail.com", "Dwi"),
        ("kunaepi.softpren@gmail.com", "Kunaepi Softpren"),
        ("test1@example.com", "Test User 1"),
        # tambah sebanyak yang kamu mau
    ]

    kirim_alert_ke_banyak(
        daftar_penerima=penerima_list,
        ip_address="182.168.1.1",
        jumlah_gagal=4,
        lokasi="Cikarang, Indonesia"
    )
