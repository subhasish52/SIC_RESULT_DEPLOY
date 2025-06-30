from flask import Flask, request, jsonify, send_from_directory, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import shutil
import traceback

app = Flask(__name__)

# ====== Configuration ======
USERNAME = "23bcsb02"
PASSWORD = "Subhasish@2006"

# ====== Paths for Render-compatible binaries ======
CHROME_BINARY = os.path.join(os.getcwd(), "bin", "chrome-linux", "chrome")
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "bin", "chromedriver")

# ====== Downloads directory ======
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# ====== Selenium Automation Logic ======
def download_pdf_for_sic(sic_number):
    print(f"[INFO] Processing SIC: {sic_number}...")

    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    options = webdriver.ChromeOptions()
    options.binary_location = CHROME_BINARY
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    try:
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"[ERROR] ChromeDriver start failed: {e}")
        print(traceback.format_exc())
        return None

    try:
        driver.get("https://erp.silicon.ac.in/estcampus/index.php")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        driver.get("https://erp.silicon.ac.in/estcampus/autonomous_exam/exam_result.php?role_code=M1Z5SEVJM2dub0NWWE5GZy82dHh2QT09")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        driver.execute_script(f"Final_Semester_Result_pdf_Download('{sic_number}')")

        timeout = 30
        start_time = time.time()
        downloaded_file = None

        while time.time() - start_time < timeout:
            for f in os.listdir(DOWNLOAD_DIR):
                if f.endswith(".pdf"):
                    downloaded_file = os.path.join(DOWNLOAD_DIR, f)
                    break
            if downloaded_file:
                break
            time.sleep(1)

        if downloaded_file:
            new_filename = f"{sic_number}.pdf"
            new_path = os.path.join(DOWNLOAD_DIR, new_filename)
            os.rename(downloaded_file, new_path)
            print(f"[SUCCESS] PDF downloaded: {new_filename}")
            return new_path
        else:
            print("[ERROR] PDF not downloaded in time.")
            return None

    except Exception as e:
        print(f"[ERROR] Failed during browser automation: {e}")
        print(traceback.format_exc())
        return None

    finally:
        driver.quit()
        print("[INFO] Selenium session ended.")

# ====== Flask Routes ======

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def download_route():
    try:
        data = request.json
        if not data or 'sic' not in data:
            return jsonify({"error": "Missing SIC number"}), 400

        raw_sic = data['sic'].strip().upper()
        if len(raw_sic) != 8:
            return jsonify({"error": "SIC must be exactly 8 characters"}), 400

        full_sic = f"SITBBS{raw_sic}"
        result_path = download_pdf_for_sic(full_sic)

        if result_path and os.path.exists(result_path):
            return jsonify({"message": "PDF downloaded successfully", "pdf": os.path.basename(result_path)})
        else:
            return jsonify({"error": "Failed to download PDF"}), 500

    except Exception as e:
        print(f"[EXCEPTION] /download: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/downloads/<filename>')
def serve_pdf(filename):
    try:
        return send_from_directory(DOWNLOAD_DIR, filename)
    except Exception as e:
        print(f"[ERROR] Serving PDF failed: {e}")
        return jsonify({"error": "PDF not found"}), 404

# ====== Start App ======
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
