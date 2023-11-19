from selenium import webdriver
import distutils
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import random
import json
import time
import re
from faker import Faker
import requests


print()
print('=============================')
print('\033[32m[+] TIDAL TOOLS | @si_bondjol\033[0m')
print('=============================')
print('\033[32m[+] NAME     : ESCOBAR')
print('\033[32m[+] LICENSI  : LIFETIME\033[0m')
print('=============================')
print()

fake = Faker()

# Membaca file json
with open('data.json', 'r') as f:
    data = json.load(f)

def print_progress(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\\r", "\\r\\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total: 
        print()




# MEMBACA USER AGENT
with open('useragent.txt', 'r') as file:
    user_agents = [line.strip() for line in file.readlines() if line.strip()]

# MEMBACA VCC
with open('vcc.txt', 'r') as file:
    first_line = file.readline().strip()
    card_number, expiry, security_code = first_line.split('|')
    expiry_month, expiry_year = expiry.split('/')

# Pastikan list user agents tidak kosong
if not user_agents:
    raise ValueError("File useragent.txt is empty.")



def is_valid_email(email):
    # Sederhana pemeriksaan format email menggunakan regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def run():
    input("[?] VPN SUDAH DI AKTIFKAN?\n[+] TEKAN ENTER JIKA SUDAH")

    continue_puppeteer(webdriver)

def continue_puppeteer(driver):
    # Menanyakan berapa banyak akun yang ingin diproses
    try:
        print()
        jumlah_akun = int(input("[?] BERAPA AKUN: "))
    except ValueError:
        print("Masukkan angka yang valid.")
        return
    # LOOP START
    for i in range(jumlah_akun):

        ## Menghasilkan email
        firstname = fake.first_name ()
        lastname = fake.last_name()
        domain = data['domain']
        email = f"{firstname}{lastname}{domain}"
        password = data['password']

        print()
        print('[+] MEMERIKSA SERVER..')

        def get_public_ip():
            response = requests.get('https://httpbin.org/ip')
            if response.status_code == 200:
                return response.json()['origin']
            else:
                return "Tidak dapat mendapatkan IP"

        def get_ip_location(ip):
            response = requests.get(f'http://ip-api.com/json/{ip}')
            if response.status_code == 200:
                data = response.json()
                return data.get('country'), data.get('city')
            else:
                return "Tidak dapat mendapatkan lokasi"

        # Mendapatkan alamat IP publik
        public_ip = get_public_ip()
        print("[+] ALAMAT IP   :", public_ip)

        # Mendapatkan lokasi dari alamat IP
        country, city = get_ip_location(public_ip)
        print(f"[+] LOKASI      : {country}, {city}")


        if country == 'Singapore':
            print('\033[32m[+] SERVER TEPAT!\033[0m')
        else:
            print('\033[31m[!] VPN YANG AKTIF BUKAN SINGAPORE!\033[0m')
            driver.quit()
            continue

        # Lanjut ke halaman Tidal
        print()
        print_progress(i + 1, jumlah_akun, prefix='[+] PROSES:', suffix='', length=50)
        print()
        print(f'[+] MEMBUAT AKUN KE-{i+1}')
        firefox_options = FirefoxOptions()
        user_agent = random.choice(user_agents)
        firefox_options.add_argument(f'user-agent={user_agent}')
        firefox_options.add_argument("-headless")  # Mengaktifkan mode headless

        # Pengaturan driver (menggunakan Firefox)
        driver = webdriver.Firefox(options=firefox_options)
        driver.get('https://offer.tidal.com/?geo=SG')
        time.sleep(3)

        # MEMERIKSA CAPTCHA
        try:
            # Mencoba mencari elemen captcha
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
            driver.switch_to.frame(iframe)
            captcha_element = driver.find_element(By.ID, 'captcha-container')
            print('\033[31m[!] CAPTCHA REACHED\033[0m')
            driver.quit()
        except NoSuchElementException:
            pass
        else:
            continue  # Melanjutkan ke iterasi berikutnya dalam loop

        print('[+] MEMERIKSA COOKIE')
        # Menunggu dan mengklik tombol terima cookie
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()
        print('[+] ACCEPTED COOKIE')

        time.sleep(2)
        link = driver.find_element(By.CSS_SELECTOR, 'a.btn-primary.margin-top-1.btn-extra-padding')
        link.click()

        # isi email n pass
        time.sleep(3)
        try:
            email_input = driver.find_element(By.ID, 'email')
            email_input.send_keys(email)
            print(f"[+] MENDAFTARKAN EMAIL : {email}")
        except:
            print("\033[33m[!] JARINGAN KURANG STABIL\033[0m")
            driver.quit()
            continue
        
        time.sleep(1)

        continue_button = driver.find_element(By.CSS_SELECTOR, 'button[ui-test-id="check-user-continue-button"]')
        continue_button.click()

        try:
            # Mencoba mencari elemen captcha
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
            driver.switch_to.frame(iframe)
            captcha_element = driver.find_element(By.ID, 'captcha-container')
            print('\033[31m[!] CAPTCHA REACHED\033[0m')
            driver.quit()
        except NoSuchElementException:
            pass
        else:
            continue  # Melanjutkan ke iterasi berikutnya dalam loop

        # Isi password
        time.sleep(5)
        try:
            password_input = driver.find_element(By.ID, 'new-password')

            password_input.send_keys(data['password'])

            # Isi confirm password
            confirm_password_input = driver.find_element(By.ID, 'password2')
            confirm_password_input.send_keys(data['confirm_password'])

            # Isi profile name
            profile_name_input = driver.find_element(By.ID, 'profileName')
            profile_name_input.send_keys(data['profile_name'])

            # Pilih tanggal lahir
            driver.find_element(By.ID, 'tbi-day').send_keys('1')

            month_dropdown = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'tbi-month'))
            )
            Select(month_dropdown).select_by_value('5')  #mei

            driver.find_element(By.ID, 'tbi-year').send_keys('2001')

            # Centang checkbox (sesuaikan selector jika perlu)
            checkbox_label = driver.find_element(By.CSS_SELECTOR, "label[for='terms1']")
            checkbox_label.click()
        except:
            print("\033[33m[!] JARINGAN KURANG STABIL/AKUN SUDAH TERDAFTAR\033[0m")
            driver.quit()
            continue

        
        time.sleep(1)
        signup_button = driver.find_element(By.CSS_SELECTOR, "button.btn-success.btn-primary")
        signup_button.click()

        # Cek keberadaan alert email tidak valid
        try:
            invalid_email_alert = WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.Vue-Toastification__toast-body"))
            )
            if "Please enter a valid email address" in invalid_email_alert.text:
                print("[!] EMAIL TIDAK VALID!")
                driver.quit()
                continue

        except:
            # Jika tidak ada alert dalam waktu 5 detik, asumsikan tidak ada masalah
            pass

        # Memeriksa CAPTCHA
        time.sleep(10)
        captcha_elements = driver.find_elements(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
        if len(captcha_elements) > 0:
            print("\033[31m[!] CAPTCHA REACHED\033[0m")
            driver.quit()
            continue

        # Menggunakan CSS Selector untuk menemukan elemen berdasarkan class
        hifi_plus_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'HiFi Plus')]"))
        )
        hifi_plus_tab.click()
        try:
            # Mencoba mencari elemen captcha
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
            driver.switch_to.frame(iframe)
            captcha_element = driver.find_element(By.ID, 'captcha-container')
            print('\033[31m[!] CAPTCHA REACHED\033[0m')
            driver.quit()
        except NoSuchElementException:
            pass
        else:
            continue  # Melanjutkan ke iterasi berikutnya dalam loop
        
        # Family
        family = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/main/div/div/div/div[2]/section[2]/ul/li[2]/div/div'))
        )
        family.click()

        # Continue
        continue2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/main/div/div/div/div[2]/section[2]/ul/li[2]/div/div/div[2]/section/div[2]/div/button'))
        )
        continue2.click()

        # MEMERIKSA CAPTCHA
        try:
            # Mencoba mencari elemen captcha
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
            driver.switch_to.frame(iframe)
            captcha_element = driver.find_element(By.ID, 'captcha-container')
            print('\033[31m[!] CAPTCHA REACHED\033[0m')
            driver.quit()
        except NoSuchElementException:
            pass
        else:
            continue  # Melanjutkan ke iterasi berikutnya dalam loop

        time.sleep(10)

        # ISI VCC
        # Mengisi nama pemegang kartu
        driver.find_element(By.NAME, 'cardholderName').send_keys('PABLO GENK')

        # Mengisi nomor kartu (berada di iframe pertama)
        iframe_card_number = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Iframe for card number"]'))
        )
        driver.switch_to.frame(iframe_card_number)
        driver.find_element(By.ID, 'encryptedCardNumber').send_keys(card_number)
        driver.switch_to.default_content()

        # Mengisi tanggal kedaluwarsa (berada di iframe kedua)
        iframe_expiry_date = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Iframe for expiry date"]'))
        )
        driver.switch_to.frame(iframe_expiry_date)
        expiry_date_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'encryptedExpiryDate'))
        )
        expiry_date_input.send_keys(f'{expiry_month}{expiry_year}')  # Format mm/yyyy
        driver.switch_to.default_content()

        # Mengisi VCC (berada di iframe ketiga)
        iframe_security_code = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Iframe for security code"]'))
        )
        driver.switch_to.frame(iframe_security_code)
        driver.find_element(By.ID, 'encryptedSecurityCode').send_keys(security_code)
        driver.switch_to.default_content()

        # Klik label yang terkait dengan checkbox
        label_for_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='autoRenewalConsentCreditCard1']"))
        )
        label_for_checkbox.click()

        # Klik tombol "Continue"
        time.sleep(5)
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continue')]"))
        )
        continue_button.click()

        time.sleep(3)
        try:
            # Mencoba mencari elemen captcha
            iframe = driver.find_element(By.XPATH, "//iframe[contains(@src, 'captcha-delivery')]")
            driver.switch_to.frame(iframe)
            captcha_element = driver.find_element(By.ID, 'captcha-container')
            print('\033[31m[!] CAPTCHA REACHED\033[0m')
            driver.quit()
        except NoSuchElementException:
            pass
        else:
            continue  # Melanjutkan ke iterasi berikutnya dalam loop

        try:
            activation_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.text-center[data-v-68d480d6]"))
            )
            # Mencetak teks dari elemen jika ditemukan dengan warna hijau
            print(f"\033[92m[+] {activation_message.text}\033[0m")
            
            # Menyimpan akun ke dalam file akun.txt
            print(f"[+] Email: {email}\n[+] Password: {password}")
            with open('akun.txt', 'a') as file:  # 'a' untuk append
                file.write(f"Email: {email}\nPassword: {password}\n\n")
            print("[+] SAVED AS akun.txt")

            # Menghapus vcc yang sudah dipakai
            with open('vcc.txt', 'r') as file:
                lines = file.readlines()
            with open('vcc.txt', 'w') as file:
                file.writelines(lines[1:])
            driver.quit()

        except TimeoutException:
            print("\033[91m[!] Your account is not activated, unsuccessfully progress or CAPTCHA reached!\033[0m")
            # Menghapus vcc yang sudah dipakai
            with open('vcc.txt', 'r') as file:
                lines = file.readlines()
            with open('vcc.txt', 'w') as file:
                file.writelines(lines[1:])
            continue

    driver.quit()
run()
