import time
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Fungsi untuk membaca token dari file
def load_tokens(file_path="tokens.txt"):
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

# Fungsi utama untuk check-in harian
def daily_checkin():
    tokens = load_tokens()  # Memuat daftar token
    options = Options()
    options.add_argument("--headless")  # Jika ingin tanpa browser UI
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    for token in tokens:
        try:
            # Inisiasi browser
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
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
                print(f"Check-in berhasil untuk token: {token}")
            except:
                print(f"Check-in gagal untuk token: {token} atau sudah check-in hari ini.")
            
            # Tunggu 5 detik sebelum memproses token berikutnya
            time.sleep(5)

        except Exception as e:
            print(f"Error pada token {token}: {e}")

        finally:
            driver.quit()

# Jadwalkan check-in harian pada pukul 07:50 WIB
schedule.every().day.at("07:50").do(daily_checkin)

# Loop untuk menjalankan schedule
while True:
    schedule.run_pending()
    time.sleep(1)
