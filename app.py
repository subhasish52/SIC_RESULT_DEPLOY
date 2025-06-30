from flask import Flask, request, jsonify, send_from_directory, render_template
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import shutil
import traceback

app = Flask(__name__)

# === ERP Credentials ===
USERNAME = "23bcsb02"
PASSWORD = "Subhasish@2006"

# === Downloads Folder ===
DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_pdf_for_sic(sic_number):
    print(f"[INFO] Starting download for: {sic_number}")
    shutil.rmtree(DOWNLOAD_DIR, ignore_errors=True)
    os.makedirs(DOWNLOAD_DIR)

    # === Chrome options ===
    options = uc.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome"  # 🔥 Critical for Render
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0")

    prefs = {
        "download.default_directory": DOWNLOAD_DIR,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    }
    options.add_experimental_option("prefs", prefs)

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        print("[INFO] Chrome session started")

        # Login Page
        driver.get("https://erp.silicon.ac.in/estcampus/index.php")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USERNAME)
        driver.find_element(By.NAME, "password").send_keys(PASSWORD)
        driver.find_element(By.XPATH, "//button[text()='Sign in']").click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Navigate to result page
        driver.get("https://erp.silicon.ac.in/estcampus/autonomous_exam/exam_result.php?role_code=M1Z5SEVJM2dub0NWWE5GZy82dHh2QT09")

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Trigger PDF download
        print(f"[INFO] Triggering PDF download for SIC: {sic_number}")
        driver.execute_script(f"Final_Semester_Result_pdf_Download('{sic_number}')")

        # Wait for download
        timeout = 45
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
            print(f"[SUCCESS] PDF saved as {new_filename}")
            return new_path
        else:
            print("[ERROR] PDF not downloaded in time.")
            return None

    except Exception as e:
        print(f"[ERROR] Download failed: {e}")
        print(traceback.format_exc())
        return None

    finally:
        try:
            driver.quit()
        except:
            pass
        print("[INFO] Chrome session closed")


# === ROUTES ===

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
            return jsonify({"message": "PDF downloaded successfully", "pdf": os.path.basename(pdf_path)})
        else:
            return jsonify({"error": "Failed to download PDF"}), 500

    except Exception as e:
        print(f"[EXCEPTION] /download: {e}")
        print(traceback.format_exc())
        return jsonify({"error": "Server error"}), 500


@app.route('/downloads/<filename>')
def serve_pdf(filename):
    try:
        return send_from_directory(DOWNLOAD_DIR, filename)
    except:
        return jsonify({"error": "PDF not found"}), 404


# === Run Local Dev Server ===
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
