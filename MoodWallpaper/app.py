"""
app.py - Main entry point for the Mood-Based Dynamic Wallpaper System.

Therapeutic Wallpaper Logic:
  Emotion   │ Goal               │ Wallpaper Theme
  ──────────┼────────────────────┼──────────────────────────────
  Happy     │ Maintain happiness │ Vibrant nature & joyful scenery
  Sad       │ Improve mood       │ Uplifting sunrise, rainbow, blossoms
  Angry     │ Calm the user      │ Tranquil ocean, still lake, zen garden
  Fear      │ Reduce anxiety     │ Warm cozy cabin, safe meadow
  Surprise  │ Maintain engagement│ Aurora, grand canyon, waterfall
  Disgust   │ Shift attention    │ Fresh flowers, clear sky, crystal water
  Neutral   │ Maintain balance   │ Mountain landscape, forest path

Workflow:
  1. Initialize logger
  2. Capture webcam image
  3. Detect face (MediaPipe)
  4. Recognize emotion (DeepFace)
  5. Log therapeutic goal & encouraging message
  6. Select matching wallpaper (therapeutic theme)
  7. Update Windows desktop wallpaper
  8. Exit
"""

import sys

from capture import capture_image
from config import setup_logging
from emotion_detector import detect_face, recognize_emotion
from mood_response import log_mood_response
from wallpaper import get_wallpaper_path, set_wallpaper


def main() -> None:
    """Execute the mood-based therapeutic wallpaper pipeline."""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("Mood-Based Dynamic Wallpaper System — Application started")
    logger.info("=" * 60)

    try:
        # ── Step 1: Capture image from webcam ────────────────────
        frame = capture_image()
        if frame is None:
            logger.error("Aborting — failed to capture image.")
            sys.exit(1)

        # ── Step 2: Detect face using MediaPipe ──────────────────
        face_found: bool = detect_face(frame)
        if not face_found:
            logger.error("Aborting — no face detected in captured image.")
            sys.exit(1)

        # ── Step 3: Recognize emotion using DeepFace ─────────────
        emotion: str | None = recognize_emotion(frame)
        if emotion is None:
            logger.error("Aborting — emotion detection failed.")
            sys.exit(1)

        # ── Step 4: Log therapeutic goal & encouraging message ────
        log_mood_response(emotion)

        # ── Step 5: Select wallpaper for therapeutic theme ────────
        wallpaper_path = get_wallpaper_path(emotion)
        if wallpaper_path is None:
            logger.error("Aborting — no wallpaper available for '%s'.", emotion)
            sys.exit(1)

        # ── Step 6: Apply wallpaper ──────────────────────────────
        success: bool = set_wallpaper(wallpaper_path)
        if not success:
            logger.error("Aborting — failed to set wallpaper.")
            sys.exit(1)

        logger.info("Wallpaper changed to support mood: %s", emotion)

    except SystemExit:
        raise

    except Exception as e:
        logger.critical("Unhandled exception: %s", e, exc_info=True)
        sys.exit(1)

    finally:
        logger.info("Application finished.")
        logger.info("=" * 60)


if __name__ == "__main__":
    main()
