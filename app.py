from flask import Flask, request, jsonify, send_from_directory, render_template
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import shutil
import traceback

app = Flask(__name__)

USERNAME = "23bcsb02"
PASSWORD = "Subhasish@2006"

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf_for_sic(sic_number):
    print(f"[INFO] Starting download for: {sic_number}")
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    chrome_binary = "/opt/render/project/src/chrome/chrome-linux64/chrome"
    chromedriver_binary = "/opt/render/project/src/chromedriver/chromedriver-linux64/chromedriver"

    options = webdriver.ChromeOptions()
    options.binary_location = chrome_binary
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--remote-debugging-port=9222")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)

    service = Service(chromedriver_binary)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("[INFO] Chrome started successfully")

        driver.get("https://erp.silicon.ac.in/estcampus/index.php")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.get("https://erp.silicon.ac.in/estcampus/autonomous_exam/exam_result.php?role_code=M1Z5SEVJM2dub0NWWE5GZy82dHh2QT09")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.execute_script(f"Final_Semester_Result_pdf_Download('{sic_number}')")

        timeout = 40
        start = time.time()
        while time.time() - start < timeout:
            for file in os.listdir(DOWNLOAD_DIR):
                if file.endswith(".pdf"):
                    new_path = os.path.join(DOWNLOAD_DIR, f"{sic_number}.pdf")
                    os.rename(os.path.join(DOWNLOAD_DIR, file), new_path)
                    return new_path
            time.sleep(1)

        print("[ERROR] PDF not found after waiting.")
        return None

    except Exception as e:
        print(f"[ERROR] Chrome failed: {e}")
        print(traceback.format_exc())
        return None

    finally:
        try:
            driver.quit()
        except:
            pass
        print("[INFO] Chrome session closed")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=["POST"])
def download_handler():
    try:
        data = request.get_json()
        sic = data.get("sic", "").strip().upper()
        if len(sic) != 8:
            return jsonify({"error": "SIC must be 8 characters"}), 400
        full_sic = f"SITBBS{sic}"
        result = download_pdf_for_sic(full_sic)
        if result:
            return jsonify({"message": "PDF downloaded", "pdf": os.path.basename(result)}), 200
        else:
            return jsonify({"error": "Failed to download PDF"}), 500
    except Exception as e:
        print(f"[EXCEPTION] {e}")
        return jsonify({"error": "Unexpected error"}), 500

@app.route('/downloads/<filename>')
def serve_pdf(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)
