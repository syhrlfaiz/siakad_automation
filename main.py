import requests
import tempfile
import os
import colorama
from colorama import Fore, Style
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.common.exceptions import NoAlertPresentException
from telegram_utils import send_telegram_message
import asyncio


colorama.init(autoreset=True)

formatted_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
SUCCESS_ALERT = Style.BRIGHT+Fore.GREEN+"[✔️]"+Fore.RESET+Style.RESET_ALL
ERROR_ALERT = Style.BRIGHT+Fore.RED+"[Error]"+Fore.RESET+Style.RESET_ALL
INFO_ALERT = Style.BRIGHT+Fore.YELLOW+"[i]"+Fore.RESET+Style.RESET_ALL
WARNING_ALERT = Style.BRIGHT+Fore.RED+"["+Fore.LIGHTYELLOW_EX+"!"+Fore.RED+"]"+Style.RESET_ALL
SUCCESS_COLOR = Fore.LIGHTGREEN_EX
INFO_COLOR = Fore.YELLOW
WARNING_COLOR = Fore.YELLOW
LINK_COLOR = Fore.LIGHTBLUE_EX
RESET_COLOR = Fore.RESET

def save_html_as_txt(response_text):
    file_path = 'login_content.txt'  # Tentukan path atau nama file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(response_text)
    return file_path

def title_info(driver):
    title = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "title"))
    )
    return title.get_attribute("innerText")

def login_info(info):
    with open(info, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        if len(lines) == 2:
            nim = lines[0].strip()
            password = lines[1].strip()
            return nim, password
        else:
            raise ValueError("File tidak ada")

def login(driver):
    login_url = 'https://siakad.stekom.ac.id/loginsiakad/login'
    login_detail = 'login_detail.txt'
    nim, password = login_info(login_detail)

    # Membuka halaman login
    driver.get(login_url)
    login_content = driver.page_source
    save_html_as_txt(login_content)
    title = title_info(driver)
    print(f"{Style.BRIGHT}{title}")

    # Buat string bintang berdasarkan panjang password
    password_print = '*' * len(password)

    # Menggunakan find_element dengan By.ID
    nim_id = driver.find_element(By.ID, "user_name")
    password_id = driver.find_element(By.ID, "user_password")
    # login_button = driver.find_element(By.TAG_NAME, "Submit")

    # Wait
    wait = 3
    time.sleep(wait)
    print(f"{INFO_ALERT}Tunggu: {INFO_COLOR}{wait} detik")

    # Input
    nim_id.send_keys(nim)
    password_id.send_keys(password)
    print(f"{SUCCESS_ALERT}Input NIM: {INFO_COLOR}{nim}{RESET_COLOR} dan password: {INFO_COLOR}{password_print}")

    # Submit
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit' and @name='Submit']"))
        )
        button.send_keys(Keys.ENTER)
        print(f"{SUCCESS_ALERT}Login Berhasil ")
    except Exception as e :
        print(f"{ERROR_ALERT}Terdapat kesalahan: {e}")
    time.sleep(wait)

def jadwal(driver):
    jadwal_url='https://siakad.stekom.ac.id/jadwalkuliahmahasiswa'
    tunggu=5
    print(f"{INFO_ALERT}Tunggu: {INFO_COLOR}{tunggu} detik")
    time.sleep(tunggu)
    
    driver.get(jadwal_url)
    print(f"{SUCCESS_ALERT}Berhasil masuk: {LINK_COLOR}{jadwal_url}")

def get_kode_kelas():
    # aktifkan ini jika ingin otomatis
    today=datetime.now().strftime("%A")
    # translate hari ke bahasa
    translate={
        "Monday": "Senin",
        "Tuesday": "Selasa",
        "Wednesday": "Rabu",
        "Thursday": "Kamis",
        "Friday": "Jumat",
        "Saturday": "Sabtu",
        "Sunday": "Minggu"
    }
    hari=translate.get(today)

    # # aktifkan ini jika ingin hari manual
    # hari = "Jumat"
    print(f"{INFO_ALERT}Hari: {Style.BRIGHT}{Fore.LIGHTYELLOW_EX}{hari}")
    
    # Mengembalikan kode kelas berdasarkan hari
    if hari == 'Senin':
        return [None]
    elif hari == 'Selasa':
        return ['54955',None]
    elif hari == 'Rabu':
        return ['54869', '53534']
    elif hari == 'Kamis':
        return ['54870', '53535']
    elif hari == 'Jumat':
        return ['54871', '54868']
    else:
        return[]
    
def title_kelas(driver):
        title_kelas_element = driver.find_element(By.XPATH, "//section[@class='content-header' and contains(@style, 'background-color:#CCCCCC')]")
        # Temukan teks info kelas
        kelas = title_kelas_element.find_element(By.XPATH, ".//strong").text
        return kelas

def masuk_absen(driver, kode_kelas):
    try:
        # Cari elemen dengan style tertentu dan teks 'kode_kelas'
        row_element = driver.find_element(By.XPATH, f"//div[@style='padding-top: 5px;padding-bottom: 5px;border-bottom: 1px solid #f4f4f4;']//strong[contains(text(), '{kode_kelas}')]")

        # Cari tombol 'Masuk Kelas' di dalam elemen yang ditemukan
        masuk_kelas_button = row_element.find_element(By.XPATH, ".//following::a[contains(@class, 'btn-sm btn-primary')]")
        kelas_link = masuk_kelas_button.get_attribute('href')

        # Arahkan driver ke link "Masuk Kelas"
        time.sleep(1)
        driver.get(kelas_link)
        print(f"{SUCCESS_ALERT}Berhasil masuk kelas: {Style.BRIGHT}{INFO_COLOR}{title_kelas(driver)}")
        print(f"{SUCCESS_ALERT}Link kelas: {LINK_COLOR}{kelas_link}")

    except Exception as e:
        print(f"{ERROR_ALERT}Kode kelas tidak ditemukan atau error: {str(e)}")

def pertemuan(driver):
    for pertemuan in range(1, 17):  # Cek dari P1 hingga P16
        berhasil = buka_pertemuan(driver, pertemuan)
        if berhasil:
            print(f"{INFO_ALERT}Absen selesai di {INFO_COLOR}Pertemuan {pertemuan}")
            print(f"{SUCCESS_ALERT}{SUCCESS_COLOR}Berhasil absen pada {INFO_COLOR}Pertemuan {pertemuan} {RESET_COLOR}- {SUCCESS_COLOR}{formatted_time}")

            break  # Berhenti jika absen berhasil
    else:
        print(f"{WARNING_ALERT}Tidak ada absensi yang ditemukan")

def handle_alert(driver):
    try:
        # Menunggu alert muncul dan menangkapnya
        alert = WebDriverWait(driver, 5).until(EC.alert_is_present())
        # alert_text = alert.text
        # print(f"{INFO_ALERT}{alert_text}")
        alert.accept()  # Menutup alert dengan mengklik OK
        print(f"{SUCCESS_ALERT}Alert berhasil ditutup")
    except NoAlertPresentException:
        print(f"{ERROR_ALERT}Tidak ada alert yang muncul")

async def buka_pertemuan(driver, pertemuan):
    try:
        # Cari elemen berdasarkan pertemuan P1, P2, ..., P16
        pertemuan_element = driver.find_element(By.XPATH, f"//span[@class='modelhp pull-right' and contains(text(), 'P{pertemuan}')]/parent::a")
        # Ambil URL dari href di elemen
        pertemuan_link = pertemuan_element.get_attribute("href")
        # print(f"Link Pertemuan P{pertemuan}: {pertemuan_link}")
        
        # Arahkan driver ke URL yang didapat
        driver.get(pertemuan_link)
        print(f"{SUCCESS_ALERT}Berhasil mengakses: {INFO_COLOR}Pertemuan {pertemuan}")
        print(f"{INFO_ALERT}Link {INFO_COLOR}Pertemuan {pertemuan}: {LINK_COLOR}{pertemuan_link}")
        # Tunggu sebentar untuk halaman load
        time.sleep(2)
        
        # Klik tab "Absensi"
        absensi_tab = driver.find_element(By.XPATH, "//a[@data-toggle='tab' and @href='#pesertakelaskelas']")
        absensi_tab.click()
        print(f"{SUCCESS_ALERT}Menuju ke {INFO_COLOR}tab 'Absensi'")

        # Tunggu agar tab Absensi terbuka
        time.sleep(2)
        
        # Coba temukan tombol absensi
        try:
            absensi_button = driver.find_element(By.XPATH, "//button[@class='btn bnt-sm btn-primary' and contains(text(), 'Absensi sekarang')]")
            absensi_button.click()
            print(f"{SUCCESS_ALERT}Berhasil klik 'Absen Sekarang'")

            print(f"{INFO_ALERT}tunggu {INFO_COLOR}5 detik")
            time.sleep(5)
            # pindah iframe
            driver.switch_to.frame("modaliframepresensi")
            print(f"{INFO_ALERT}switch iframe")

            # Klik elemen label Baik
            baik_element = driver.find_element(By.XPATH, "//label[@onclick='cekdata(2)']")
            baik_element.click()
            print(f"{SUCCESS_ALERT}Berhasil klik opsi 'Baik'")

            try:
                time.sleep(2)
                # Coba temukan elemen 'Akan Hadir'
                akan_hadir_button = driver.find_element(By.XPATH, "//li[@id='pp1']")
                # Klik elemen tersebut
                akan_hadir_button.click()
                print(f"{SUCCESS_ALERT}Berhasil klik 'Akan Hadir'")

            except NoSuchElementException:
                print(f"{WARNING_ALERT}Tombol 'Akan Hadir' tidak ditemukan, melanjutkan ke langkah berikutnya.")


            # Tunggu hingga tombol Absen Daring (Online) muncul, lalu klik
            absen_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@onclick='simpanreview(1)']"))
            )

            absen_button.click()
            print(f"{SUCCESS_ALERT}Berhasil klik tombol 'Absen Daring (Online)'")

            driver.switch_to.default_content()
            print(f"{SUCCESS_ALERT}Berhasil keluar dari iframe")

            handle_alert(driver)

            message = (f"🔔SIAKAD AUTOMATION🔔\n"
                       f"\n"
                       f"BERHASIL ABSEN [✓]\n"
                       f"``````````````````\n"
                       f"✏️ {title_kelas(driver)}\n"
                       f"📍Pertemuan {pertemuan}"
                       f"⏰{formatted_time}")
            await send_telegram_message(message)

            return True  # Berhasil absen
        except:
            try:
                # Periksa keberadaan elemen alert 'SUDAH PRESENSI'
                driver.find_element(By.XPATH, "//div[@class='alert alert-success']")
                print(f"{SUCCESS_ALERT}{SUCCESS_COLOR}Sudah Absen pada {INFO_COLOR}Pertemuan {pertemuan}")
            except NoSuchElementException:
                print(f"{WARNING_ALERT}Dosen Belum mengupload materi")
            return False 

    except Exception as e:
        print(f"{ERROR_ALERT}Error pada Pertemuan P{pertemuan}: {str(e)}")
    return False  # Ada kesalahan


def absen(driver):
    kode_kelas_1, kode_kelas_2=get_kode_kelas()
    if kode_kelas_1:
        print(f"{INFO_ALERT}Kode Kelas: {INFO_COLOR}{kode_kelas_1}")
        masuk_absen(driver, kode_kelas_1)
        time.sleep(5)
        pertemuan(driver) #memanggil pertemuan
        time.sleep(5)
        print(f"{INFO_ALERT}kembali ke Jadwal untuk mengakses kelas berikutnya")
        jadwal(driver)
    if kode_kelas_2:
        time.sleep(5)
        print(f"{INFO_ALERT}Kode Kelas: {INFO_COLOR}{kode_kelas_2}")
        masuk_absen(driver, kode_kelas_2)
        time.sleep(5)
        pertemuan(driver) #memanggil pertemuan
        time.sleep(5)

def main():
    options = Options()
    options.binary_location = "/usr/bin/brave-browser"

    # Headless option(agar tidak ada GUI) | nonaktifkan jika ingin dengan GUI
    options.add_argument("--headless") # Tambahkan opsi headless
    options.add_argument("--no-sandbox") # Untuk menjalankan dalam container
    options.add_argument("--disable-dev-shm-usage") # Untuk mengatasi error resource
    options.add_argument("--disable-gpu") # Nonaktifkan GPU
    options.add_argument("--window-size=1920,1080") 

    # Inisialisasi webdriver
    service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Panggil fungsi login
        login(driver)
        jadwal(driver)
        absen(driver)
        print(f"{SUCCESS_ALERT}{SUCCESS_COLOR}Proses selesai tanpa error.")
    
    except Exception as e:
        print(f"{ERROR_ALERT}Terjadi error: {e}")
    
    finally:
        if driver:
            try:
                driver.close()  # Tutup tab yang aktif
                driver.quit()   # Tutup seluruh sesi browser
                print(f"{WARNING_ALERT}Browser dan driver ditutup.")
            except Exception as e:
                print(f"Error saat menutup browser: {e}")

if __name__ == "__main__":
    main()
