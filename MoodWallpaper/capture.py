"""
capture.py - Webcam capture module for Mood-Based Dynamic Wallpaper System.

Handles webcam initialization, frame capture, and resource cleanup.
"""

import logging

import cv2
import numpy as np

from config import CAMERA_INDEX, CAMERA_WARMUP_FRAMES

logger = logging.getLogger("MoodWallpaper")


def capture_image() -> np.ndarray | None:
    """Open the webcam, capture a single frame, and return it.

    Discards a few initial frames to allow the camera's auto-exposure
    and white-balance to stabilize before capturing the final image.

    Returns:
        np.ndarray | None: The captured BGR image, or None on failure.
    """
    cap: cv2.VideoCapture | None = None

    try:
        logger.info("Initializing webcam (index=%d)...", CAMERA_INDEX)
        cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

        if not cap.isOpened():
            logger.error("Camera unavailable — could not open device %d.", CAMERA_INDEX)
            return None

        logger.info("Camera initialized successfully.")

        # Discard warm-up frames for auto-exposure stabilization
        for _ in range(CAMERA_WARMUP_FRAMES):
            cap.read()

        ret, frame = cap.read()

        if not ret or frame is None:
            logger.error("Failed to capture image from webcam.")
            return None

        logger.info(
            "Image captured successfully (resolution: %dx%d).",
            frame.shape[1],
            frame.shape[0],
        )
        return frame

    except cv2.error as e:
        logger.error("OpenCV error during capture: %s", e)
        return None

    except Exception as e:
        logger.error("Unexpected error during capture: %s", e)
        return None

    finally:
        if cap is not None:
            cap.release()
            logger.info("Webcam released.")
