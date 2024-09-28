import requests
import tempfile
import os
import time
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
    login_detail = 'login_detail.txt'
    nim, password = login_info(login_detail)

    # Buat string bintang berdasarkan panjang password
    password_print = '*' * len(password)

    # Menggunakan find_element dengan By.ID
    nim_id = driver.find_element(By.ID, "user_name")
    password_id = driver.find_element(By.ID, "user_password")
    # login_button = driver.find_element(By.TAG_NAME, "Submit")

    # Wait
    wait = 3
    time.sleep(wait)
    print(f"tunggu {wait} detik sebelum input NIM: {nim} dan password: {password_print}")

    # Input
    nim_id.send_keys(nim)
    password_id.send_keys(password)

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

def main():
    login_url = 'https://siakad.stekom.ac.id/loginsiakad/login'
    
    options = Options()
    options.binary_location = "/usr/bin/brave-browser"

    # Inisialisasi webdriver
    service = Service('/usr/local/bin/chromedriver-linux64/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    # Membuka halaman login
    driver.get(login_url)
    login_content = driver.page_source
    save_html_as_txt(login_content)
    title = title_info(driver)
    print(f"{title}")

    # Panggil fungsi login
    login(driver)

if __name__ == "__main__":
    main()
