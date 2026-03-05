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
BASE_URL = os.getenv("BASE_URL")

def buat_pesan_html(email_penerima, nama_pengguna, ip_address, waktu, jumlah_gagal, lokasi):
    """Membuat konten email dalam format HTML agar lebih meyakinkan."""
    token = str(uuid.uuid4())[:12]
    tracking_link = f"{BASE_URL}/track?token={token}&email={email_penerima}"
   
    # Template HTML dengan tambahan footer resmi Bank Mandiri
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 25px; background: #fff;">
            <h2 style="color: #00467E; margin-bottom: 5px;">PT Bank Mandiri (Persero) Tbk</h2>
            <p style="margin: 0; font-size: 14px;">Halo <strong>{nama_pengguna}</strong>,</p>
            
            <p>Kami mendeteksi adanya percobaan login yang tidak biasa pada akun Livin' by Mandiri Anda.</p>
            
            <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0;">
                <p style="margin: 0 0 10px 0; font-weight: bold;">Detail Kejadian:</p>
                <ul style="margin: 5px 0; padding-left: 20px;">
                    <li>Waktu: {waktu}</li>
                    <li>IP Address: {ip_address}</li>
                    <li>Lokasi: {lokasi}</li>
                    <li>Upaya Gagal: {jumlah_gagal} kali</li>
                </ul>
            </div>
            
            <p style="margin: 25px 0;">
                Untuk memastikan keamanan akun Anda, mohon segera verifikasi aktivitas ini:
            </p>
            
            <p style="text-align: center; margin: 25px 0;">
                <a href="{tracking_link}"
                   style="background: #fb8c00; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                   Verifikasi Aktivitas Sekarang
                </a>
            </p>
            
            <p style="font-size: 13px; color: #555; margin: 20px 0;">
                Jika ini bukan Anda yang melakukan percobaan login tersebut, segera hubungi Mandiri Call untuk bantuan lebih lanjut.
            </p>
            
            <!-- Footer resmi Bank Mandiri -->
            <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 11px; color: #666;">
                <p style="margin: 0 0 8px 0; font-weight: bold;">Headquarters</p>
                <p style="margin: 0;">Menara Mandiri 1<br>Jenderal Sudirman Street Kav 54-55<br>Jakarta 12190 Indonesia</p>
                <p style="margin: 8px 0;">Phone: 14000, +62-21-52997777<br>SWIFT Code: BMRIIDJA</p>
                
                <p style="margin: 12px 0 8px 0;">
                    Bank Mandiri berizin dan diawasi oleh Otoritas Jasa Keuangan (OJK) & Bank Indonesia (BI).<br>
                    Bank Mandiri adalah anggota Lembaga Penjamin Simpanan (LPS). Nilai simpanan yang dijamin LPS maksimal Rp2 miliar per nasabah per bank.<br>
                    Untuk mengecek Tingkat Bunga Penjaminan LPS, silakan klik <a href="https://www.lps.go.id/tingkat-bunga-penjaminan/" style="color: #00467E;">di sini</a>.
                </p>
                
                <p style="margin: 15px 0 5px 0; font-weight: bold;">Hubungi Kami:</p>
                <p style="margin: 3px 0;">
                    • Email: <a href="mailto:mandiricare@bankmandiri.co.id" style="color: #00467E;">mandiricare@bankmandiri.co.id</a><br>
                    • Facebook: facebook.com/BankMandiri<br>
                    • Twitter: twitter.com/bankmandiri<br>
                    • WhatsApp MITA: +62 811-1400-140<br>
                    • Mandiri Call: 14000<br>
                    • Hubungi Kami: <a href="https://www.bankmandiri.co.id/hubungi-kami" style="color: #00467E;">www.bankmandiri.co.id/hubungi-kami</a>
                </p>
                
                <p style="margin-top: 15px; font-size: 10px; color: #888; text-align: center;">
                    Email ini dikirim secara otomatis oleh sistem keamanan Bank Mandiri. Mohon tidak membalas email ini.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content, tracking_link


def kirim_alert_massal(daftar_penerima, ip_address="Tidak diketahui", jumlah_gagal=1, lokasi="Tidak diketahui"):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S WIB")
   
    try:
        # Buka koneksi SMTP sekali saja
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
                msg['Subject'] = "Peringatan Keamanan: Percobaan Login Tidak Dikenal"
                
                html_body, _ = buat_pesan_html(email, nama, ip_address, waktu, jumlah_gagal, lokasi)
                msg.attach(MIMEText(html_body, 'html'))
                
                server.sendmail(SENDER_EMAIL, email, msg.as_string())
               
                sukses_count += 1
                print(f"[{sukses_count}/{total}] Terkirim ke: {email}")
               
                time.sleep(0.8)  # Delay anti-spam Gmail
                
            except Exception as e:
                print(f"Gagal mengirim ke {email}: {e}")
                
        server.quit()
        print(f"\nSelesai! Berhasil mengirim: {sukses_count}/{total}")
        
    except Exception as e:
        print(f"Gagal koneksi ke server SMTP: {e}")


if __name__ == "__main__":
    penerima_list = [
        ("pitrasukmadi212@gmail.com", "Pitrasukmadi212"),
        ("vinoardawijaya25@gmail.com", "Vinoardawijaya25"),
        ("asaanggoro258@gmail.com", "Asaanggoro258"),
        ("selamanyaashari@gmail.com", "Selamanyaashari"),
        ("asrisarilestari327@gmail.com", "Asrisarilestari327"),
        ("csudarno3@gmail.com", "Csudarno3"),
        ("ddsupriadi30@gmail.com", "Ddsupriadi30"),
        ("derryrekayasa@yahoo.co.id", "Derryrekayasa"),
        ("diankristya80@gmail.com", "Diankristya80"),
        ("ramdani16hs@gmail.com", "Ramdani16hs"),
        ("Khansa.azahra2@gmail.com", "Khansa Azahra2"),
        ("fhandayani699@gmail.com", "Fhandayani699"),
        ("fresisumartini292@gmail.com", "Fresisumartini292"),
        ("har_tommo@yahoo.co.id", "Har Tommo"),
        ("spmheru03@gmail.com", "Spmheru03"),
        ("dennydenok00@gmail.com", "Dennydenok00"),
        ("irwanfauzi424@gmail.com", "Irwanfauzi424"),
        ("johannsyah36@gmail.com", "Johannsyah36"),
        ("hudamiftkhul25@gmail.com", "Hudamiftkhul25"),
        ("p.nuraini11@yahoo.com", "P Nuraini11"),
        ("pujisuryanto100@gmail.com", "Pujisuryanto100"),
        ("rajunugroho1@gmail.com", "Rajunugroho1"),
        ("rikkedyah01@gmail.com", "Rikkedyah01"),
        ("risyantoro95@gmail.com", "Risyantoro95"),
        ("sandradepvi@gmail.com", "Sandradepvi"),
        ("sitihumaeroh305@gmail.com", "Sitihumaeroh305"),
        ("sromlahh08@gmail.com", "Sromlahh08"),
        ("silvialdilarahmah@gmail.com", "Silvialdilarahmah"),
        ("zsyaifudin38@gmail.com", "Zsyaifudin38"),
        ("wahyu.novian96@gmail.com", "Wahyu Novian96"),
        ("febri.yosi@yahoo.com", "Febri Yosi"),
        ("gentasewu@gmail.com", "Gentasewu"),
        ("reikirei162@gmail.com", "Reikirei162"),
        ("lutfialamin82@gmail.com", "Lutfialamin82"),
        ("ajisaputra2903@gmail.com", "Ajisaputra2903"),
        ("ardiansyahhutasuhut384@gmail.com", "Ardiansyahhutasuhut384"),
        ("Riskinugrahasena@gmail.com", "Riskinugrahasena"),
        ("jejensugianto123@gmail.com", "Jejensugianto123"),
        ("rizalnugraha441@gmail.com", "Rizalnugraha441"),
        ("taufiqhidaya2000@gmail.com", "Taufiqhidaya2000"),
        ("irfanaziz180890@gmail.com", "Irfanaziz180890"),
        ("zaenalmuhtar07@gmail.com", "Zaenalmuhtar07"),
        ("Fanifitriani70@gmail.com", "Fanifitriani70"),
        ("chiellomett305@gmail.com", "Chiellomett305"),
        ("melaniizhar12@gmail.com", "Melaniizhar12"),
        ("sryyuliharyati@gmail.com", "Sryyuliharyati"),
        ("muhammadizam420@gmail.com", "Muhammadizam420"),
        ("simamoradisco@gmail.com", "Simamoradisco"),
        ("ahmadsukronmasum@gmail.com", "Ahmadsukronmasum"),
        ("rintosilalahi7@gmail.com", "Rintosilalahi7"),
        ("Imambaehaqi0895@gmail.com", "Imambaehaqi0895"),
        ("zayinaufaauladi99@gmail.com", "Zayinaufaauladi99"),
        ("dwistyawan1998@gmail.com", "Dwistyawan1998"),
        ("imamnursidik36@gmail.com", "Imamnursidik36"),
        ("Itaayu0923@gmail.com", "Itaayu0923"),
        ("hikmatnugraha.nugraha@gmail.com", "Hikmatnugraha Nugraha"),
        ("dikoalfauzi57@gmail.com", "Dikoalfauzi57"),
        ("yuniarto6288@gmail.com", "Yuniarto6288"),
        ("saep.udin09090@gmail.com", "Saep Udin09090"),
        ("wikisusilo007@gmail.com", "Wikisusilo007"),
        ("rhyuselvidwi@gmail.com", "Rhyuselvidwi"),
        ("Warionugraha12@gmail.com", "Warionugraha12"),
        ("viakhusnul28@gmail.com", "Viakhusnul28"),
        ("arisutriwinarni@gmail.com", "Arisutriwinarni"),
        ("edisupriadie87@gmail.com", "Edisupriadie87"),
        ("muhammadsoleh565@gmail.com", "Muhammadsoleh565"),
        ("indraballitha201@gmail.com", "Indraballitha201"),
        ("cahyasabrut23@gmail.com", "Cahyasabrut23"),
        ("handiharyadi17@gmail.com", "Handiharyadi17"),
        ("mfahrudinsaputra@gmail.com", "Mfahrudinsaputra"),
        ("parisrivalce45@gmail.com", "Parisrivalce45"),
        ("fmustofa654@gmail.com", "Fmustofa654"),
        ("udinsolah412@gmail.com", "Udinsolah412"),
        ("ifanmohamad54@gmail.com", "Ifanmohamad54"),
        ("muhamadnuh1975@gmail.com", "Muhamadnuh1975"),
        ("mulyadidimas9@gmail.com", "Mulyadidimas9"),
        ("teguhdeliyanto635@gmail.com", "Teguhdeliyanto635"),
        ("fnugraha172@gmail.com", "Fnugraha172"),
        ("indanaa702@gmail.com", "Indanaa702"),
        ("amirsarifudi92@gmail.com", "Amirsarifudi92"),
        ("adianggasetiawan20000516@gmail.com", "Adianggasetiawan20000516"),
        ("robbyzakaria180@gmail.com", "Robbyzakaria180"),
        ("sdozan17@gmail.com", "Sdozan17"),
        ("mulyananirya8@gmail.com", "Mulyananirya8"),
        ("nuryanihlusytasari0845@gmail.com", "Nuryanihlusytasari0845"),
        ("apepsaepul233@gmail.com", "Apepsaepul233"),
        ("agryardianjauhari@gmail.com", "Agryardianjauhari"),
        ("jepara.indah10@gmail.com", "Jepara Indah10"),
        ("novalgumelar24@gmail.com", "Novalgumelar24"),
        ("herlianaintan3@gmail.com", "Herlianaintan3"),
        ("hafsyahsyabrina@gmail.com", "Hafsyahsyabrina"),
        ("wulansulistyorini@gmail.com", "Wulansulistyorini"),
        ("putri.aoliya29@gmail.com", "Putri Aoliya29"),
        ("otnayamoeba@gmail.com", "Otnayamoeba"),
        ("kunaepi21@gmail.com", "Kunaepi21"),
    ]
    
    kirim_alert_massal(
        penerima_list,
        ip_address="192.168.1.1",      # Ganti sesuai kebutuhan
        jumlah_gagal=3,
        lokasi="Jakarta, Indonesia"    # Ganti sesuai kebutuhan
    )
