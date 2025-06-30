## 📘 **SIC Result Viewer**

*A fully automated PDF fetcher for student results from Silicon University's ERP portal, built with Python, Flask, Selenium, and deployed on Render.*

---

### 📖 Table of Contents

* [📜 About the Project](#-about-the-project)
* [⚙️ Features](#️-features)
* [🚀 Live Demo](#-live-demo)
* [🛠️ Tech Stack](#️-tech-stack)
* [📂 Folder Structure](#-folder-structure)
* [🧪 How It Works](#-how-it-works)
* [🔧 Setup Instructions (Local)](#-setup-instructions-local)
* [🌐 Deployment (Render)](#-deployment-render)
* [🧠 Future Ideas](#-future-ideas)
* [📬 Contact](#-contact)

---

### 📜 About the Project

> The **SIC Result Viewer** is a sleek, modern web interface to fetch **autonomous semester result PDFs** directly from your university's ERP portal using just your 8-character SIC number.
> It uses real-time **headless browser automation**, **PDF rendering**, and a cool animated UI — all deployed in the cloud.

---

### ⚙️ Features

✅ Enter SIC number → get result instantly
✅ Real-time PDF download from ERP
✅ Modern dark-themed UI with glassmorphism
✅ 3D loading animation with fading effects
✅ Fully hosted on [Render.com](https://render.com)
✅ Mobile responsive & user-friendly

---

### 🚀 Live Demo

🌐 **Try it here:**
[https://sic-result-deploy.onrender.com](https://sic-result-deploy.onrender.com)

---

### 🛠️ Tech Stack

| Layer      | Tech                   |
| ---------- | ---------------------- |
| Frontend   | HTML, CSS, JavaScript  |
| Backend    | Flask                  |
| Automation | Selenium, ChromeDriver |
| Rendering  | headless Chrome        |
| Deployment | Render                 |

---

### 📂 Folder Structure

```
SIC_RESULT_DEPLOY/
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── downloads/         # Auto-created for PDFs
├── app.py             # Flask + Selenium backend
├── build.sh           # Chrome & ChromeDriver setup
├── requirements.txt
├── render.yaml
└── README.md          # ← You are here
```

---

### 🧪 How It Works

1. You enter your 8-char SIC number (e.g. `23BCSB02`)
2. Flask formats it to `SITBBS23BCSB02`
3. Selenium logs in to ERP using stored credentials
4. Navigates to result page and downloads your PDF
5. PDF is renamed and displayed on-screen
6. You view/download it directly from browser ✅

---

### 🔧 Setup Instructions (Local)

#### 1. Clone the repo

```bash
git clone https://github.com/subhasish52/SIC_RESULT_DEPLOY.git
cd SIC_RESULT_DEPLOY
```

#### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Or venv\Scripts\activate on Windows
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Run it locally

```bash
python app.py
```

---

### 🌐 Deployment (Render)

**🧰 render.yaml**

```yaml
services:
  - type: web
    name: sic-result-deploy
    runtime: python
    buildCommand: "pip install -r requirements.txt && ./build.sh"
    startCommand: "gunicorn app:app"
    plan: free
    envVars: []
```

**✅ Notes**

* Chrome v123 and matching ChromeDriver are installed using `build.sh`
* No environment variables needed (but you can add `.env` later for secrets)

---

### 🧠 Future Ideas

* [ ] Add CGPA extractor from PDF
* [ ] Login authentication
* [ ] Send PDF to email
* [ ] Multiple SIC inputs for batch download
* [ ] Smart PDF renaming
* [ ] Caching of previously fetched results

---

### 📬 Contact

📛 **Author:** Subhasish
🎓 B.Tech CSE @ Silicon University
🌐 [GitHub](https://github.com/subhasish52)
✉️ DM on Discord or Telegram for collab/projects
