from flask import Flask, request, redirect
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TARGET_URL = "https://www.mandiri.co.id/keamanan"  # ganti ke halaman real nanti

@app.route('/track')
def track():
    email = request.args.get('email')
    token = request.args.get('token')
    if not email or not token:
        return "Link tidak valid", 400

    ip = request.remote_addr
    ua = request.headers.get('User-Agent', 'Unknown')
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")

    log_msg = f"DIKLIK | Email: {email} | Token: {token} | IP: {ip} | Device: {ua} | {waktu}"
    print(log_msg)  # Ini pasti ke stdout → muncul di logs Railway

    # Optional: app.logger.info(log_msg) kalau pakai Flask logger

    return redirect(TARGET_URL)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

    app.run(debug=True)


