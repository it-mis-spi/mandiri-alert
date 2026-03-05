from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

# Setup Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key-jika-tidak-ada")

# Setup logging agar muncul di Railway logs (stdout)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]  # Pastikan ke stdout
)
logger = logging.getLogger(__name__)

# Halaman tujuan setelah klik link
TARGET_URL = "https://www.mandiri.co.id/keamanan"  # Ganti sesuai kebutuhan

@app.route('/track')
def track():
    """
    Endpoint untuk tracking klik link dari email alert.
    Mencatat email, token, IP, User-Agent (device/browser), dan waktu.
    """
    email = request.args.get('email')
    token = request.args.get('token')

    if not email or not token:
        logger.warning("Akses /track tanpa email atau token")
        return "Link tidak valid", 400

    # Ambil data request
    ip = request.remote_addr or "Unknown"
    ua = request.headers.get('User-Agent', 'Unknown')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")

    # Buat pesan log
    log_msg = (
        f"DIKLIK | "
        f"Email: {email} | "
        f"Token: {token} | "
        f"IP: {ip} | "
        f"Device/User-Agent: {ua} | "
        f"Waktu: {waktu}"
    )

    # Cetak ke stdout (pasti muncul di Railway Deploy Logs atau HTTP Logs)
    print(log_msg)

    # Log dengan level INFO (bisa difilter di dashboard)
    logger.info(log_msg)

    # Optional: kalau ingin log ke file (tapi di Railway ephemeral, hilang saat restart)
    # with open('/tmp/klik.log', 'a') as f:
    #     f.write(log_msg + '\n')

    # Redirect ke halaman keamanan
    return redirect(TARGET_URL)

@app.route('/')
def home():
    """Route root sederhana untuk test apakah app hidup"""
    return "Server Mandiri Alert Tracking aktif. Gunakan /track?token=...&email=..."

if __name__ == '__main__':
    # Untuk test lokal saja (di Railway ini diabaikan karena pakai Gunicorn)
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False di production
