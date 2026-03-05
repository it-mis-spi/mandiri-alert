from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key-ubah-ini")

# Setup logging ke stdout (Railway capture ini di Deploy Logs / HTTP Logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Halaman tujuan setelah klik
TARGET_URL = "https://www.mandiri.co.id/keamanan"  # Ganti sesuai halaman real

@app.route('/track')
def track():
    """
    Tracking klik link dari email.
    Catat email, token, IP, User-Agent (device), waktu.
    """
    email = request.args.get('email')
    token = request.args.get('token')

    if not email or not token:
        logger.warning("Akses /track tanpa parameter email/token")
        return "Link tidak valid", 400

    ip = request.remote_addr or "Unknown"
    ua = request.headers.get('User-Agent', 'Unknown')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")

    log_msg = (
        f"DIKLIK | "
        f"Email: {email} | "
        f"Token: {token} | "
        f"IP: {ip} | "
        f"Device/User-Agent: {ua} | "
        f"Waktu: {waktu}"
    )

    # Cetak ke stdout (pasti muncul di Railway logs)
    print(log_msg)
    # Log Flask-level
    logger.info(log_msg)

    return redirect(TARGET_URL)

@app.route('/')
def home():
    """Route sederhana untuk test app hidup"""
    return "Server Mandiri Alert Tracking aktif. Akses /track?token=...&email=... untuk test."

if __name__ == '__main__':
    # Hanya untuk test lokal (di Railway ini diabaikan oleh Gunicorn)
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # debug=False di production
