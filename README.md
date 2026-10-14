# 🛡️ TransitGuard AI

**Privacy-Preserving Edge AI for Micro-Accessibility and Safety in Public Transit Hubs**

TransitGuard AI is a lightweight Edge AI prototype designed to detect micro-accessibility barriers in train and bus stations—specifically wheelchair ramps obstructed by luggage, platform overcrowding, and maintenance faults—while upholding passenger privacy through 100% offline edge processing and zero facial recognition.

---

## 🏗️ Project Architecture (Stage 1 Initial Structure)

```text
TransitGuard-AI/
├── app.py                      # Streamlit Home & System Overview
├── config.py                   # Central settings, thresholds, and palette
├── requirements.txt            # Python dependencies (Streamlit, YOLO, OpenCV, etc.)
├── .gitignore                  # Keeps large weights and local DBs out of git
├── LICENSE                     # MIT License
├── .streamlit/
│   └── config.toml             # Custom Dark Navy & Blue Streamlit theme
├── pages/
│   ├── 1_AI_Detection.py       # Pretrained YOLO Object Detection (Stage 2)
│   ├── 2_Ramp_Monitoring.py    # Ramp ROI & Luggage Obstruction (Stage 3)
│   ├── 3_Crowd_Monitoring.py   # Crowd Density & Zone Bottlenecks (Stage 4)
│   ├── 4_Alerts.py             # Incident Feed & SQLite Dashboard (Stage 6)
│   ├── 5_Maintenance.py        # Manual Infrastructure Reports (Stage 6)
│   └── 6_Privacy_Centre.py     # Privacy Principles & Face Blurring (Stage 5)
├── sample_images/              # Test images for ramps and crowds
└── tests/
    └── test_basic.py           # Configuration tests
```

---

## ⚡ Quick Start Guide (Stage 1)

### 1. Open Terminal and Navigate to Project
```powershell
cd C:\Users\Lenovo\.gemini\antigravity\scratch\TransitGuard-AI
```

### 2. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
*(If PowerShell restricts script execution, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` or use Command Prompt `venv\Scripts\activate.bat`)*

### 3. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```powershell
streamlit run app.py
```

The application will launch automatically in your browser at `http://localhost:8501`.
