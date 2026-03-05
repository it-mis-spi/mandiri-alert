import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")

def kirim_alert_bulk(emails_list, nama_pengguna_list, ip_address, jumlah_gagal, lokasi="Tidak diketahui"):
    """Kirim alert ke banyak email sekaligus (personalized)"""
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    
    for email_penerima, nama in zip(emails_list, nama_pengguna_list):
        message = Mail(
            from_email='mandiricare.livinapp@gmail.com',  # Verifikasi dulu di SendGrid
            to_emails=email_penerima,
            subject="MANDIRI CARE - Peringatan: Percobaan Login Ilegal",
            plain_text_content=f"""
Halo {nama},

Ada percobaan login ilegal ke akun Anda.

Detail:
- Waktu: {datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")}
- IP: {ip_address}
- Lokasi: {lokasi}
- Jumlah gagal: {jumlah_gagal}

Segera cek & amankan akun Anda.

Tim Mandiri Care
            """
        )
        
        try:
            response = sg.send(message)
            print(f"SUKSES ke {email_penerima} - Status: {response.status_code}")
        except Exception as e:
            print(f"GAGAL ke {email_penerima}: {e}")

# Contoh pakai (banyak email)
if __name__ == "__main__":
    emails = ["kunaepi21@gmail.com", "dwi.softpren@gmail.com", "test1@gmail.com"]  # list email penerima
    namas = ["Kunaepi", "Dwi", "Test User"]  # list nama sesuai urutan
    kirim_alert_bulk(emails, namas, "182.168.1.1", 5)
