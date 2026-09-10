# 🔒 Face Biometric Unlock Screen with Voice Greeting ("Hello <MyName>")

A modern, responsive desktop Lock/Unlock screen application powered by computer vision (OpenCV LBPH facial recognition) and offline voice synthesis (Windows SAPI5 / `pyttsx3`).

---

## ✨ Features

- **Biometric Face Recognition**:
  - Automatically identifies registered users in real time using OpenCV's Local Binary Patterns Histograms (LBPH) and CLAHE contrast enhancement.
  - Multi-frame temporal consensus prevents accidental unlocks or false flickers.
- **Voice Greeting**:
  - Greet authorized users out loud when unlocked: *"Hello [MyName]! Access granted. Welcome back."*
  - Uses Windows native SAPI5 speech synthesis (100% offline, zero cloud delays or privacy issues).
- **Modern Dark UI (CustomTkinter)**:
  - Futuristic biometric scanning viewport with animated scanlines, live digital clock, calendar date, and HUD target brackets.
- **Fail-Safe Security**:
  - Backup PIN authentication (Default: `1234` or custom PIN set during registration).
  - Emergency bypass shortcut: `Esc` to exit fullscreen, or close button.
- **One-Click Face Enrollment**:
  - Built-in enrollment wizard captures 35 sample angles and retrains the model in under 2 seconds.
- **Unlocked Dashboard**:
  - Displays session details, user profiles, voice test button, and a "Lock Screen Now" button for instant testing.

---

## 🚀 Quick Start

### 1. Launch the Application
Double-click `run.bat` or run in terminal:
```bash
cd C:\Users\ASUS\.gemini\antigravity\scratch\face_unlock_app
python main.py
```

### 2. Enroll Your Face
1. On initial startup, the **Face Biometric Enrollment Wizard** will automatically open.
2. Enter your name (e.g. `Alex`) and optional backup PIN.
3. Click **▶ Start Face Scan**.
4. Look at the camera while the progress bar fills from 0% to 100% (35 samples captured).
5. The neural model will train instantly (< 2 seconds) and confirm registration.
6. Click **✔ Done - Go to Lock Screen**.

### 3. Unlock with Your Face!
- Look directly into the camera on the Lock Screen.
- The biometric scanner will recognize your face, turn vibrant green, play an unlock chime, and announce:
  > *"Hello Alex! Access granted. Welcome back."*
- The screen unlocks to your Dashboard!

---

## ⌨️ Shortcuts & Controls

| Key / Control | Action |
| --- | --- |
| `F11` | Toggle Fullscreen / Windowed mode |
| `Esc` | Exit Fullscreen |
| `🔑 Unlock with PIN` | Enter backup PIN (`1234`) if camera is covered |
| `🔒 Lock Now` | Instantly lock the screen again from the dashboard |

---

## 🗑️ How to Delete Existing Faces

You have 3 easy ways to delete face profiles:

### Method 1: Directly from the Dashboard UI (Recommended)
1. Unlock the screen to access the Dashboard.
2. In the **Enrolled Face Profiles & Settings** section at the bottom, each enrolled profile is listed.
3. Click the red **🗑️ Delete** button next to any profile to delete only that user.
4. Or click **🗑️ Reset All Faces** in the top right to erase all profiles and start fresh.

### Method 2: Using the Cleanup Script
Run the interactive cleaner in terminal:
```bash
python reset_faces.py
```
It will display all enrolled profiles and ask for confirmation to wipe them.

### Method 3: Manual Deletion via File Explorer
If you want to manually delete the files:
1. Delete all images inside `face_unlock_app/data/`.
2. Delete `face_unlock_app/model/users.json` and `face_unlock_app/model/face_recognizer.yml`.

---

## 📂 Project Structure

```
face_unlock_app/
│── assets/
│   └── haarcascade_frontalface_default.xml   # Pre-bundled face detector
│── data/                                     # User face training crops
│── model/
│   ├── face_recognizer.yml                   # Trained LBPH facial model
│   └── users.json                            # Registered user profiles
│── tests/
│   └── test_core.py                          # Automated test suite
│── config.py                                 # App configuration & thresholds
│── face_engine.py                            # Detection, LBPH training & inference
│── voice_engine.py                           # Async pyttsx3 voice engine
│── ui_draw.py                                # Sci-fi HUD brackets & scanlines
│── ui_lock_screen.py                         # Lock screen view with camera & clock
│── ui_enroll.py                              # Face enrollment wizard
│── ui_dashboard.py                           # Unlocked state dashboard
│── main.py                                   # Master application launcher
│── run.bat                                   # One-click Windows runner
│── requirements.txt                          # Python dependencies
└── README.md
```
