# 🎭 Mood-Based Dynamic Wallpaper System

A Windows desktop application that **automatically detects your facial emotion** via webcam and **changes your desktop wallpaper** to match your current mood.

---

## ✨ Features

| Feature | Details |
|---------|---------|
| **Webcam Capture** | Opens camera, captures one frame, and releases immediately |
| **Face Detection** | MediaPipe Face Detection for fast, reliable detection |
| **Emotion Recognition** | DeepFace analyzes 7 emotions: Happy, Sad, Angry, Neutral, Fear, Surprise, Disgust |
| **Wallpaper Update** | Uses Windows API (`SystemParametersInfoW`) to set the desktop wallpaper |
| **Logging** | Full activity log saved to `logs/app.log` |
| **Error Handling** | Graceful handling of all failure scenarios |

---

## 📁 Project Structure

```
MoodWallpaper/
│
├── app.py                  # Main entry point — orchestrates the pipeline
├── capture.py              # Webcam initialization and frame capture
├── emotion_detector.py     # Face detection (MediaPipe) + emotion analysis (DeepFace)
├── wallpaper.py            # Wallpaper selection and Windows API update
├── config.py               # Configuration: paths, logging, constants
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── wallpapers/             # Wallpaper images organized by emotion
│   ├── happy/
│   ├── sad/
│   ├── angry/
│   ├── neutral/
│   ├── fear/
│   ├── surprise/
│   └── disgust/
│
└── logs/                   # Application logs
    └── app.log
```

---

## 🛠️ Installation

### Prerequisites

- **Python 3.11+** installed on your system
- **Windows 10/11**
- A working **webcam**

### Step 1 — Clone or download the project

```bash
git clone <repository-url>
cd MoodWallpaper
```

### Step 2 — Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** The first run may take a minute as DeepFace downloads the emotion model (~25 MB).

---

## 🚀 Running the Application

```bash
python app.py
```

### What happens:

1. The webcam opens briefly (≈1 second).
2. One photo is captured.
3. Your face is detected via MediaPipe.
4. Your emotion is analyzed via DeepFace.
5. A matching wallpaper is randomly selected.
6. Your Windows desktop wallpaper is updated.
7. The application exits.

**Total execution time:** < 5 seconds on a typical laptop.

---

## 🖼️ Adding Your Own Wallpapers

Place wallpaper images in the corresponding emotion folder:

```
wallpapers/
├── happy/       ← Put cheerful, bright wallpapers here
├── sad/         ← Put moody, rain, melancholic wallpapers here
├── angry/       ← Put intense, fiery wallpapers here
├── neutral/     ← Put calm, balanced wallpapers here
├── fear/        ← Put dark, mysterious wallpapers here
├── surprise/    ← Put vibrant, spectacular wallpapers here
└── disgust/     ← Put grim, muted wallpapers here
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`, `.bmp`, `.webp`

> **Tip:** Use high-resolution images (1920×1080 or above) for the best desktop experience.

---

## 🔄 Auto-Run on Login (Optional)

To automatically run the application after Windows login:

### Method 1 — Startup Folder

1. Press `Win + R` and type `shell:startup`
2. Create a shortcut to a batch file or directly to `python app.py`
3. Example batch file (`mood_wallpaper.bat`):

```bat
@echo off
cd /d "C:\path\to\MoodWallpaper"
call venv\Scripts\activate
python app.py
```

### Method 2 — Task Scheduler

1. Open **Task Scheduler** → Create Basic Task
2. Set trigger to **At log on**
3. Set action to **Start a program**
4. Program: `C:\path\to\MoodWallpaper\venv\Scripts\python.exe`
5. Arguments: `app.py`
6. Start in: `C:\path\to\MoodWallpaper`

---

## 📋 Emotion → Wallpaper Mapping

| Emotion | Wallpaper Theme | Example |
|---------|----------------|---------|
| 😊 Happy | Bright sunrises, beaches, sunflowers | Warm golden tones |
| 😢 Sad | Rainy cities, foggy lakes | Cool blue-grey tones |
| 😠 Angry | Volcanoes, thunderstorms | Intense red-orange |
| 😐 Neutral | Mountains, zen gardens | Balanced earth tones |
| 😨 Fear | Dark forests, abandoned places | Deep blue-black |
| 😲 Surprise | Auroras, fireworks | Vivid neon colors |
| 🤢 Disgust | Wastelands, swamps | Muted green-grey |

---

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Camera not detected** | Ensure webcam is connected and not in use by another app. Try changing `CAMERA_INDEX` in `config.py`. |
| **No face detected** | Ensure proper lighting and face the camera directly. |
| **Emotion detection fails** | Ensure `deepface` and `tf-keras` are properly installed. Check `logs/app.log` for details. |
| **Wallpaper not changing** | Verify that wallpaper images exist in the correct emotion folder. Check supported extensions. |
| **Permission errors** | Run the application with appropriate user permissions. |
| **Slow first run** | DeepFace downloads models on first use — this is normal and only happens once. |
| **Import errors** | Make sure you activated the virtual environment: `venv\Scripts\activate` |

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `opencv-python` | Webcam access and image processing |
| `mediapipe` | Face detection |
| `deepface` | Emotion recognition |
| `tf-keras` | TensorFlow backend for DeepFace |

---

## 📝 Logs

All activity is logged to `logs/app.log`:

```
2026-07-15 15:30:01 | INFO     | Application started
2026-07-15 15:30:01 | INFO     | Camera initialized successfully.
2026-07-15 15:30:02 | INFO     | Image captured successfully (resolution: 1280x720).
2026-07-15 15:30:02 | INFO     | Face detected (1 face(s) found).
2026-07-15 15:30:03 | INFO     | Emotion detected: happy
2026-07-15 15:30:03 | INFO     | Wallpaper selected: happy_sunrise.png
2026-07-15 15:30:03 | INFO     | Wallpaper updated successfully.
2026-07-15 15:30:03 | INFO     | Application finished.
```

---

## 📄 License

This project is for educational and personal use.
