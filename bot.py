import time
import jwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Fungsi untuk membaca token dari file
def load_tokens(file_path="tokens.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Fungsi untuk decode token JWT (meskipun tidak digunakan di sini, untuk konsistensi)
def get_username_from_token(token):
    try:
        # Decode JWT token (tanpa verifikasi untuk tujuan ini)
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("userId", "Nama Pengguna Tidak Ditemukan")
    except Exception as e:
        print(f"Error mendecode token: {e}")
        return "Error Mendecode Token"

# Fungsi utama untuk check-in harian
def daily_checkin():
    tokens = load_tokens()  # Memuat daftar token
    options = Options()
    options.add_argument("--headless")  # Menjalankan Firefox tanpa UI
    options.add_argument("--no-sandbox")

    for idx, token in enumerate(tokens, start=1):  # Menggunakan `enumerate` untuk memberi nomor pada akun
        driver = None
        try:
            # Menyusun nama akun seperti Akun 1, Akun 2, dll.
            username = f"Akun {idx}"

            # Inisiasi browser Firefox
            driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
            driver.get("https://dropair.io/")
            
            # Set auth-token sebagai cookie untuk login
            driver.add_cookie({
                "name": "auth-token",
                "value": token,
                "path": "/",
                "domain": ".dropair.io"
            })
            
            # Refresh halaman agar cookie diterapkan
            driver.refresh()
            time.sleep(3)  # Tunggu agar halaman ter-load dengan baik

            # Mencari tombol check-in
            try:
                checkin_button = driver.find_element(By.XPATH, "//button[contains(@class, 'bg-[#15ef93]') and contains(text(), 'Start')]")
                checkin_button.click()
                print(f"Check-in berhasil untuk {username}")
            except:
                print(f"Check-in gagal untuk {username} atau sudah check-in hari ini.")
            
            # Tunggu 5 detik sebelum memproses token berikutnya
            time.sleep(5)

        except Exception as e:
            print(f"Error pada token {token}: {e}")

        finally:
            if driver is not None:
                driver.quit()

# Loop untuk melakukan check-in setiap 24 jam
while True:
    daily_checkin()
    print("Menunggu 24 jam sebelum check-in berikutnya...")
    time.sleep(86400)  # Tunggu selama 24 jam (86400 detik)
