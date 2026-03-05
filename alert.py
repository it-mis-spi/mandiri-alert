import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from datetime import datetime
from dotenv import load_dotenv
import uuid
import time

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
BASE_URL = os.getenv ("BASE_URL")

def buat_pesan_html(email_penerima, nama_pengguna, ip_address, waktu, jumlah_gagal, lokasi):
    """Membuat konten email dalam format HTML agar lebih meyakinkan."""
    token = str(uuid.uuid4())[:12]
    tracking_link = f"{BASE_URL}/track?token={token}&email={email_penerima}"
    
    # Template HTML Sederhana (Bisa kamu percantik lagi dengan CSS)
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <div style="max-width: 600px; border: 1px solid #ddd; padding: 20px;">
            <h2 style="color: #00467E;">MANDIRI CARE</h2>
            <p>Halo <strong>{nama_pengguna}</strong>,</p>
            <p>Kami mendeteksi adanya percobaan login yang tidak biasa pada akun Livin' Anda.</p>
            <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
                <p><strong>Detail Kejadian:</strong></p>
                <ul>
                    <li>Waktu: {waktu}</li>
                    <li>IP Address: {ip_address}</li>
                    <li>Lokasi: {lokasi}</li>
                    <li>Upaya Gagal: {jumlah_gagal} kali</li>
                </ul>
            </div>
            <p style="margin-top: 20px;">
                <a href="{tracking_link}" 
                   style="background: #fb8c00; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                   Verifikasi Aktivitas Sekarang
                </a>
            </p>
            <p style="font-size: 12px; color: #888; margin-top: 30px;">
                Jika ini bukan Anda, segera hubungi Mandiri Call 14000.
            </p>
        </div>
    </body>
    </html>
    """
    return html_content, tracking_link

def kirim_alert_massal(daftar_penerima, ip_address="Tidak diketahui", jumlah_gagal=1, lokasi="Tidak diketahui"):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
    
    try:
        # 1. Buka koneksi SMTP SEKALI saja di awal
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        sukses_count = 0
        total = len(daftar_penerima)

        for email, nama in daftar_penerima:
            try:
                msg = MIMEMultipart()
                msg['From'] = f"Mandiri Care <{SENDER_EMAIL}>"
                msg['To'] = email
                msg['Subject'] = "Peringatan Keamanan: Percobaan Login Ilegal"

                html_body, _ = buat_pesan_html(email, nama, ip_address, waktu, jumlah_gagal, lokasi)
                msg.attach(MIMEText(html_body, 'html'))

                # 2. Kirim tanpa perlu login ulang
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
                
                sukses_count += 1
                print(f"[{sukses_count}/{total}] Terkirim ke: {email}")
                
                # Delay kecil agar Gmail tidak curiga (0.5 - 1 detik cukup)
                time.sleep(0.8) 
                
            except Exception as e:
                print(f"Gagal mengirim ke {email}: {e}")

        # 3. Tutup koneksi setelah semua selesai
        server.quit()
        print(f"\nSelesai! Berhasil: {sukses_count}/{total}")

    except Exception as e:
        print(f"Gagal koneksi ke server SMTP: {e}")

if __name__ == "__main__":
    penerima_list = [
        ("kunaepi21@gmail.com", "Kunaepi"),
        ("dwi.softpren@gmail.com", "Dwi"),
        # Tambahkan list lainnya di sini
    ]

    kirim_alert_massal(
        penerima_list, 
        ip_address="192.168.1.1", 
        jumlah_gagal=3, 
        lokasi="Jakarta, Indonesia"
    )




