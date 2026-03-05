from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default-secret-key")

# Konfigurasi Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Ambil URL tujuan dari env atau default
TARGET_URL = os.getenv("TARGET_URL", "mandiri-alert-production.up.railway.app")

@app.route('/track')
def track():
    email = request.args.get('email')
    token = request.args.get('token')

    if not email or not token:
        logger.warning("Akses /track tanpa parameter lengkap")
        return "Parameter tidak lengkap", 400

    # Mendapatkan IP asli dibalik proxy Railway
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = (
        f"LOG_TRACK | "
        f"Email: {email} | "
        f"Token: {token} | "
        f"IP: {ip} | "
        f"Waktu: {waktu} | "
        f"UA: {ua}"
    )

    logger.info(log_msg)

    # Redirect user ke halaman asli
    return redirect(TARGET_URL)

@app.route('/')
def home():
    return "Service Active"

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

