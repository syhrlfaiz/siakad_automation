import requests
import tempfile
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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
    print(f"{title}")

    # Buat string bintang berdasarkan panjang password
    password_print = '*' * len(password)

    # Menggunakan find_element dengan By.ID
    nim_id = driver.find_element(By.ID, "user_name")
    password_id = driver.find_element(By.ID, "user_password")
    # login_button = driver.find_element(By.TAG_NAME, "Submit")

    # Wait
    wait = 3
    time.sleep(wait)
    print(f"tunggu {wait} detik")

    # Input
    nim_id.send_keys(nim)
    password_id.send_keys(password)
    print(f"input NIM: {nim} dan password: {password_print}")

    # Submit
    try:
        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit' and @name='Submit']"))
        )
        button.send_keys(Keys.ENTER)
        print("Berhasil login")
    except Exception as e :
        print(f"Terdapat kesalahan: {e}")
    time.sleep(wait)

def jadwal(driver):
    jadwal_url='https://siakad.stekom.ac.id/jadwalkuliahmahasiswa'
    tunggu=5
    print(f"tunggu {tunggu} detik")
    time.sleep(tunggu)
    
    driver.get(jadwal_url)
    print(f"berhasil akses : {jadwal_url}")

def get_kode_kelas():
    # # aktifkan ini jika ingin otomatis
    # today=datetime.now().strftime("%A")
    # # translate hari ke bahasa
    # translate={
    #     "Monday": "Senin",
    #     "Tuesday": "Selasa",
    #     "Wednesday": "Rabu",
    #     "Thursday": "Kamis",
    #     "Friday": "Jumat",
    #     "Saturday": "Sabtu",
    #     "Sunday": "Minggu"
    # }
    # hari=translate.get(today)

    # aktifkan ini jik ingin hari manual
    hari = "Rabu"
    print(f"hari : {hari}")
    
    # Mengembalikan kode kelas berdasarkan hari
    if hari == 'Senin':
        return [None]
    elif hari == 'Selasa':
        return ['54955']
    elif hari == 'Rabu':
        return ['54869', '53534']
    elif hari == 'Kamis':
        return ['54870', '53535']
    elif hari == 'Jumat':
        return ['54871', '54868']
    else:
        return[]

def masuk_absen(driver, kode_kelas):
    try:
        # Cari elemen dengan style tertentu dan teks 'kode_kelas'
        row_element = driver.find_element(By.XPATH, f"//div[@style='padding-top: 5px;padding-bottom: 5px;border-bottom: 1px solid #f4f4f4;']//strong[contains(text(), '{kode_kelas}')]")

        # Cari tombol 'Masuk Kelas' di dalam elemen yang ditemukan
        masuk_kelas_button = row_element.find_element(By.XPATH, ".//following::a[contains(@class, 'btn-sm btn-primary')]")
        kelas_link = masuk_kelas_button.get_attribute('href')

        print(f"Link Masuk Kelas: {kelas_link}")

        # Arahkan driver ke link "Masuk Kelas"
        driver.get(kelas_link)
        print(f"Berhasil mengakses: {kelas_link}")

    except Exception as e:
        print(f"Kode kelas tidak ditemukan atau error: {str(e)}")

def absen(driver):
    kode_kelas_1, kode_kelas_2=get_kode_kelas()
    if kode_kelas_1:
        print(f"masuk {kode_kelas_1}")
        masuk_absen(driver, kode_kelas_1)

        time.sleep(5)
        jadwal(driver)
    if kode_kelas_2:
        print(f"masuk {kode_kelas_2}")
        masuk_absen(driver, kode_kelas_2)

def main():
    options = Options()
    options.binary_location = "/usr/bin/brave-browser"

    # Inisialisasi webdriver
    service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
    driver = None

    try:
        driver = webdriver.Chrome(service=service, options=options)
        
        # Panggil fungsi login
        login(driver)
        jadwal(driver)
        absen(driver)
        print("Proses selesai tanpa error.")
    
    except Exception as e:
        print(f"Terjadi error: {e}")
    
    finally:
        if driver:
            try:
                driver.close()  # Tutup tab yang aktif
                driver.quit()   # Tutup seluruh sesi browser
                print("Browser dan driver ditutup.")
            except Exception as e:
                print(f"Error saat menutup browser: {e}")

if __name__ == "__main__":
    main()
