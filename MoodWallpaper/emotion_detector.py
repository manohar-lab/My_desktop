"""
emotion_detector.py - Face detection and emotion recognition module.

Uses MediaPipe Tasks API for face detection and DeepFace for emotion analysis.
"""

import logging

import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace

from config import FACE_MODEL_PATH

logger = logging.getLogger("MoodWallpaper")


def detect_face(image: np.ndarray) -> bool:
    """Detect whether at least one face is present in the image.

    Uses the MediaPipe Tasks Vision API (FaceDetector) with the
    blaze_face_short_range model for fast and reliable detection.

    Args:
        image: BGR image captured from the webcam.

    Returns:
        True if at least one face is detected, False otherwise.
    """
    try:
        if not FACE_MODEL_PATH.exists():
            logger.error("Face detection model not found: %s", FACE_MODEL_PATH)
            return False

        BaseOptions = mp.tasks.BaseOptions
        FaceDetector = mp.tasks.vision.FaceDetector
        FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
        VisionRunningMode = mp.tasks.vision.RunningMode

        options = FaceDetectorOptions(
            base_options=BaseOptions(model_asset_path=str(FACE_MODEL_PATH)),
            running_mode=VisionRunningMode.IMAGE,
            min_detection_confidence=0.5,
        )

        with FaceDetector.create_from_options(options) as detector:
            # MediaPipe Tasks expects RGB input wrapped in mp.Image
            rgb_image: np.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)

            result = detector.detect(mp_image)

            if result.detections:
                logger.info(
                    "Face detected (%d face(s) found).", len(result.detections)
                )
                return True

            logger.warning("No face detected in the captured image.")
            return False

    except Exception as e:
        logger.error("Error during face detection: %s", e)
        return False


def recognize_emotion(image: np.ndarray) -> str | None:
    """Analyze the captured image and return the dominant emotion.

    Uses DeepFace with enforce_detection=False so that the analysis
    proceeds even when the built-in detector has marginal confidence.

    Args:
        image: BGR image captured from the webcam.

    Returns:
        The dominant emotion as a lowercase string, or None on failure.
    """
    try:
        logger.info("Analyzing emotion...")

        results = DeepFace.analyze(
            img_path=image,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="skip",
            silent=True,
        )

        # DeepFace.analyze returns a list of dicts (one per detected face)
        if isinstance(results, list):
            analysis = results[0]
        else:
            analysis = results

        dominant_emotion: str = analysis["dominant_emotion"].lower()
        emotion_scores: dict = analysis.get("emotion", {})

        logger.info("Emotion detected: %s", dominant_emotion)
        logger.info("Emotion scores: %s", emotion_scores)

        return dominant_emotion

    except ValueError as e:
        logger.error("Emotion detection failed — no face found by DeepFace: %s", e)
        return None

    except Exception as e:
        logger.error("Unexpected error during emotion recognition: %s", e)
        return None
