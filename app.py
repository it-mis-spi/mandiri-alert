from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "mandiri-secure-key-2024")

# Konfigurasi Logging agar muncul di Railway Dashboard
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Ambil URL tujuan dari env. WAJIB pakai https://
TARGET_URL = os.getenv("TARGET_URL", "https://www.bankmandiri.co.id/")

@app.route('/track')
def track():
    # 1. Ambil Parameter (Gunakan default 'Unknown' jika kosong)
    email = request.args.get('email', 'Unknown')
    token = request.args.get('token', 'NoToken')

    # 2. Ambil Informasi Koneksi (IP Asli & Device)
    # Railway menggunakan proxy, jadi ambil dari X-Forwarded-For
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()
    ua = request.headers.get('User-Agent', 'Unknown')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")

    # 3. MENCATAT LOG (Paling Penting)
    # Kita cetak pakai logger DAN print agar pasti masuk ke tab Logs Railway
    log_msg = f"--- TARGET DIKLIK ---\nEmail: {email}\nToken: {token}\nIP: {ip}\nWaktu: {waktu}\nDevice: {ua}\n----------------------"
    print(log_msg) 
    logger.info(log_msg)

    # 4. REDIRECT KE HALAMAN ASLI
    # Pastikan domain tujuan punya protokol http/https
    final_destination = TARGET_URL if TARGET_URL.startswith("http") else f"https://{TARGET_URL}"
    return redirect(final_destination)

@app.route('/')
def home():
    return "Mandiri Tracking Service is Online."

if __name__ == '__main__':
    # Cek IP Publik Server saat dinyalakan (untuk debugging)
    try:
        server_ip = requests.get('https://api.ipify.org').text
        print(f"Server started on IP: {server_ip}")
    except:
        pass

    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
