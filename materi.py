import asyncio
from telegram_utils import telegram_bot  # Assumes telegram_utils.py exists in your project
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from main import login, jadwal  # Importing the login and jadwal functions from main.py

def select_kode_kelas():
    print("Pilih kode kelas:")
    print("1. Administrator Jaringan dan Database [54955]")
    print("2. Aplikasi Pemrograman Web [54869]")
    print("3. Metode Penelitian [54870]")
    print("4. Aplikasi Pemrograman Visual [54871]")
    print("5. Rekayasa Perangkat Lunak 2 [53535]")
    print("6. Pemrogrraman Mobile 2 [54871]")
    print("7. Technoprenuership [54868]")
    pilihan = input("Masukkan pilihan (angka): ")

    kode_kelas_dict = {
        "1": "54955",
        "2": "54869",
        "3": "54870",
        "4": "54871",
        "5": "53535",
        "6": "54871",
        "7": "54868"
    }
    return kode_kelas_dict.get(pilihan, None)

def fetch_class_and_material_links(driver, kode_kelas):
    material_links = {}
    try:
        row_element = driver.find_element(By.XPATH, f"//div[@style='padding-top: 5px;padding-bottom: 5px;border-bottom: 1px solid #f4f4f4;']//strong[contains(text(), '{kode_kelas}')]")
        masuk_kelas_button = row_element.find_element(By.XPATH, ".//following::a[contains(@class, 'btn-sm btn-primary')]")
        kelas_link = masuk_kelas_button.get_attribute('href')

        driver.get(kelas_link)
        kelas_title = driver.find_element(By.XPATH, "//section[@class='content-header']//strong").text
        print(f"Berhasil masuk kelas: {kelas_title}")

        for pertemuan in range(1, 17):  # Loop through sessions 1 to 16
            try:
                session_element = driver.find_element(By.XPATH, f"//span[@class='modelhp pull-right' and contains(text(), 'P{pertemuan}')]/parent::a")
                session_link = session_element.get_attribute('href')
                driver.get(session_link)

                # Switch to the "Diskusi" tab
                diskusi_tab = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@data-toggle='tab' and @href='#Forum' and contains(@onclick, 'tabmenu')]"))
                )
                diskusi_tab.click()
                print(f"Berhasil mengakses tab 'Diskusi' untuk Pertemuan {pertemuan}")

                # Fetch the material link in the "Diskusi" tab
                try:
                    materi_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, "//div[@class='overlay-video']/a[@class='popup-youtube video-play-button']"))
                    )
                    materi_link = materi_element.get_attribute('href')
                    material_links[pertemuan] = materi_link
                    print(f"Link materi Pertemuan {pertemuan}: {materi_link}")
                except (NoSuchElementException, TimeoutException):
                    material_links[pertemuan] = "Dosen belum mengupload materi"
                    print(f"Materi tidak ditemukan di Pertemuan {pertemuan}. Menghentikan pengecekan lebih lanjut.")
                    break  # Stop checking further sessions if the material link is not found

            except Exception as e:
                print(f"Error pada Pertemuan {pertemuan}: {e}")
                material_links[pertemuan] = "Dosen belum mengupload materi"
                break  # Stop checking further sessions if there is an error

    except Exception as e:
        print(f"Error saat mencoba masuk ke kelas {kode_kelas}: {e}")
    
    return kelas_title, material_links

def send_class_info_to_telegram(kode_kelas, kelas_title, material_links):
    message = f"🔔 **Link Materi** 🔔\n\nKode Kelas: {kode_kelas}\n\n\n**{kelas_title}**\n\n"
    for pertemuan, link in material_links.items():
        message += f"📍 Pertemuan {pertemuan}: {link}\n"

    telegram_bot.send_telegram(message)

def main():
    options = Options()
    options.binary_location = "/usr/bin/brave-browser"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
    driver = None

    try:
        kode_kelas = select_kode_kelas()  # Prompt the user to select the class code at the start
        if not kode_kelas:
            print("Pilihan tidak valid. Silakan coba lagi.")
            return  # Exit the script if the user input is invalid

        driver = webdriver.Chrome(service=service, options=options)
        login(driver)  # Use the login function from main.py
        jadwal(driver)  # Use the jadwal function from main.py to access the schedule

        kelas_title, material_links = fetch_class_and_material_links(driver, kode_kelas)
        send_class_info_to_telegram(kode_kelas, kelas_title, material_links)

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

    finally:
        if driver:
            driver.close()
            driver.quit()
            print("Browser dan driver telah ditutup.")

if __name__ == "__main__":
    main()
