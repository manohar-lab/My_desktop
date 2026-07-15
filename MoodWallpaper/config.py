"""
config.py - Configuration module for Mood-Based Dynamic Wallpaper System.

Stores application-wide settings including directory paths,
logging configuration, and supported file extensions.
"""

import logging
from pathlib import Path

# ─── Base Directories ────────────────────────────────────────────────
BASE_DIR: Path = Path(__file__).resolve().parent
WALLPAPER_DIR: Path = BASE_DIR / "wallpapers"
LOG_DIR: Path = BASE_DIR / "logs"
LOG_FILE: Path = LOG_DIR / "app.log"

# ─── Supported Emotions ─────────────────────────────────────────────
EMOTIONS: list[str] = [
    "happy",
    "sad",
    "angry",
    "neutral",
    "fear",
    "surprise",
    "disgust",
]

# ─── Supported Image Extensions ─────────────────────────────────────
SUPPORTED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

# ─── MediaPipe Face Detection Model ─────────────────────────────────
FACE_MODEL_PATH: Path = BASE_DIR / "blaze_face_short_range.tflite"

# ─── Camera Settings ────────────────────────────────────────────────
CAMERA_INDEX: int = 0
CAMERA_WARMUP_FRAMES: int = 5  # Discard initial frames for auto-exposure

# ─── Logging Configuration ──────────────────────────────────────────
LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(message)s"
LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
LOG_LEVEL: int = logging.INFO


def setup_logging() -> logging.Logger:
    """Configure and return the application logger.

    Creates the log directory if it does not exist and sets up
    both file and console handlers with the configured format.

    Returns:
        logging.Logger: Configured logger instance.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("MoodWallpaper")
    logger.setLevel(LOG_LEVEL)

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
