# Filament Tracker

## Overview
Filament Tracker is a **Flask-based web app** for managing **3D printing filament usage and print jobs**.  
It tracks **filament rolls**, logs **print jobs**, and integrates with **PrusaSlicer** to automatically import print data.  

## How to Run

### 🚀 Docker (Recommended)
1. **Pull and Run the Container:**
   ```bash
   docker-compose up -d
   ```
2. **Access the Web App:**  
   Open `http://localhost:5000` (or the IP/port combination of your docker host) in your browser.

### 🛠️ Manual Setup (Development)
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run the app:**
   ```bash
   flask run
   ```
3. **Access:**  
   Open `http://localhost:5000` in your browser.

---

## 🔹 PrusaSlicer Integration
Filament Tracker can automatically capture **filament usage and project names** from **PrusaSlicer** using a post-processing script.

### ✅ How It Works
1. When you slice a model in **PrusaSlicer**, it executes `prusa_post.py` as a post-processing script.
2. This script extracts relevant metadata from the generated G-code file, such as:
   - **Filament weight (g)**
   - **Project name (from filename or PrusaSlicer environment variables)**
   - **Slicing timestamp**
3. The extracted data is sent to Filament Tracker as an **unreviewed print job**, where you can assign a filament roll and finalize it.

### 🔧 Setting Up the Integration
#### **1️⃣ Add the Post-Processing Script in PrusaSlicer**
1. Open **PrusaSlicer**.
2. Go to **Printer Settings → Custom G-code → Post-processing scripts**.
3. Add the following command (adjust the path to your script):
   ```
   "C:\Users\YourUser\path\to\python.exe" "C:\path\to\prusa_post.py"
   ```
   - Replace `C:\Users\YourUser\path\to\python.exe` with your actual Python path.
   - Replace `C:\path\to\prusa_post.py` with the actual script location.
   - Edit

#### **2️⃣ How to Manually Run `prusa_post.py` (Testing)**
You can manually run the script to test how it processes a G-code file:
```bash
python prusa_post.py "C:\path\to\your_model.gcode"
```
If successful, you should see:
```plaintext
Processing G-code: your_model.gcode
Data extracted and sent to Filament Tracker.
```

#### **3️⃣ Assigning the Unreviewed Print Jobs**
1. Open Filament Tracker (`http://localhost:5000`).
2. Under **Unreviewed Print Jobs**, find the newly added entry.
3. Click **Approve**, select the correct filament roll, adjust values if needed, and save the print job.