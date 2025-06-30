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

# Define download directory
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

# Path to Chrome binary on Render
CHROME_BINARY = "/usr/bin/chromium"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"

# ====== Selenium Automation ======
def download_pdf_for_sic(sic_number):
    print(f"[INFO] Processing SIC: {sic_number}...")

    # Clear previous files
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    # Chrome Options
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
        print("[INFO] ChromeDriver started.")
    except Exception as e:
        print(f"[ERROR] Failed to start ChromeDriver: {e}")
        print(traceback.format_exc())
        return None

    try:
        # Go to login
        driver.get("https://erp.silicon.ac.in/estcampus/index.php")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        ).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        # Wait for body after login
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Go to result page
        result_url = "https://erp.silicon.ac.in/estcampus/autonomous_exam/exam_result.php?role_code=M1Z5SEVJM2dub0NWWE5GZy82dHh2QT09"
        driver.get(result_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        print(f"[INFO] Downloading PDF for {sic_number}")
        driver.execute_script(f"Final_Semester_Result_pdf_Download('{sic_number}')")

        # Wait for file to appear
        timeout = 30
        start = time.time()
        downloaded_file = None

        while time.time() - start < timeout:
            for filename in os.listdir(DOWNLOAD_DIR):
                if filename.endswith(".pdf"):
                    downloaded_file = os.path.join(DOWNLOAD_DIR, filename)
                    break
            if downloaded_file:
                break
            time.sleep(1)

        if downloaded_file:
            new_filename = f"{sic_number}.pdf"
            final_path = os.path.join(DOWNLOAD_DIR, new_filename)
            os.rename(downloaded_file, final_path)
            print(f"[SUCCESS] PDF downloaded and renamed to {new_filename}")
            return final_path
        else:
            print("[WARNING] PDF not found after timeout.")
            return None

    except Exception as e:
        print(f"[ERROR] During automation: {e}")
        print(traceback.format_exc())
        return None
    finally:
        driver.quit()
        print("[INFO] Browser closed.")

# ====== Flask Routes ======

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.json
        if not data or 'sic' not in data:
            return jsonify({"error": "No SIC number provided"}), 400

        sic = data['sic'].strip().upper()
        if len(sic) != 8:
            return jsonify({"error": "SIC must be exactly 8 characters"}), 400

        full_sic = f"SITBBS{sic}"
        pdf_path = download_pdf_for_sic(full_sic)

        if pdf_path and os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path)
            return jsonify({"message": "PDF downloaded successfully", "pdf": filename}), 200
        else:
            return jsonify({"error": "Failed to download PDF"}), 500

    except Exception as e:
        print(f"[ERROR] in /download: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error"}), 500

@app.route('/downloads/<filename>')
def serve_pdf(filename):
    try:
        return send_from_directory(DOWNLOAD_DIR, filename)
    except Exception as e:
        print(f"[ERROR] Serving file: {e}")
        return jsonify({"error": "File not found"}), 404

# ====== Run App ======
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
