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

# ====== ERP Login Credentials ======
USERNAME = "23bcsb02"
PASSWORD = "Subhasish@2006"

# ====== Chromium & Driver Paths for Render ======
CHROME_BINARY = os.path.join(os.getcwd(), "bin", "chrome-linux", "chrome")
CHROMEDRIVER_PATH = os.path.join(os.getcwd(), "bin", "chromedriver")

# ====== PDF Output Directory ======
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_pdf_for_sic(sic_number):
    print(f"[INFO] Processing SIC: {sic_number}...")

    # Clear previous downloads
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = CHROME_BINARY
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option("prefs", {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })

    try:
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("[INFO] Selenium started.")
    except Exception as e:
        print(f"[ERROR] Failed to launch Chrome: {e}")
        print(traceback.format_exc())
        return None

    try:
        # Login flow
        driver.get("https://erp.silicon.ac.in/estcampus/index.php")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Go to result page
        driver.get("https://erp.silicon.ac.in/estcampus/autonomous_exam/exam_result.php?role_code=M1Z5SEVJM2dub0NWWE5GZy82dHh2QT09")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Execute download script
        driver.execute_script(f"Final_Semester_Result_pdf_Download('{sic_number}')")

        # Wait for PDF
        timeout = 30
        start_time = time.time()
        downloaded_file = None

        while time.time() - start_time < timeout:
            for file in os.listdir(DOWNLOAD_DIR):
                if file.endswith(".pdf"):
                    downloaded_file = os.path.join(DOWNLOAD_DIR, file)
                    break
            if downloaded_file:
                break
            time.sleep(1)

        if downloaded_file:
            new_filename = f"{sic_number}.pdf"
            new_path = os.path.join(DOWNLOAD_DIR, new_filename)
            os.rename(downloaded_file, new_path)
            return new_path
        else:
            print("[ERROR] PDF not found after timeout.")
            return None

    except Exception as e:
        print(f"[EXCEPTION] Error during download: {e}")
        print(traceback.format_exc())
        return None

    finally:
        driver.quit()

# ====== Flask Routes ======

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/download', methods=['POST'])
def handle_download():
    try:
        data = request.json
        if not data or "sic" not in data:
            return jsonify({"error": "Missing SIC number"}), 400

        user_input = data["sic"].strip().upper()
        if len(user_input) != 8:
            return jsonify({"error": "SIC must be 8 characters"}), 400

        full_sic = f"SITBBS{user_input}"
        pdf_path = download_pdf_for_sic(full_sic)

        if pdf_path and os.path.exists(pdf_path):
            return jsonify({"message": "PDF downloaded successfully", "pdf": os.path.basename(pdf_path)}), 200
        else:
            return jsonify({"error": "PDF generation failed"}), 500

    except Exception as e:
        print(f"[EXCEPTION] /download: {e}")
        return jsonify({"error": "Server error"}), 500

@app.route('/downloads/<filename>')
def serve_pdf(filename):
    try:
        return send_from_directory(DOWNLOAD_DIR, filename)
    except:
        return jsonify({"error": "PDF not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
