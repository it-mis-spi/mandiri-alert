from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Load env vars
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-ubah-ini")

# Logging ke stdout (Railway capture di Deploy Logs / HTTP Logs)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

TARGET_URL = "https://www.bankmandiri.co.id/"  # Ganti ke halaman real nanti

@app.route('/track')
def track():
    email = request.args.get('email')
    token = request.args.get('token')

    if not email or not token:
        logger.warning("Akses /track tanpa email atau token")
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

    # Cetak ke stdout (pasti muncul di logs Railway)
    print(log_msg)
    logger.info(log_msg)  # Level INFO untuk filter mudah

    return redirect(TARGET_URL)

@app.route('/')
def home():
    return "Server Mandiri Alert Tracking aktif. Gunakan /track?token=...&email=... untuk test."

if __name__ == '__main__':
    # Hanya untuk test lokal (Railway pakai Gunicorn, ini diabaikan)
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
