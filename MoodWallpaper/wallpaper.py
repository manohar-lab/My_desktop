"""
wallpaper.py - Wallpaper selection and Windows desktop update module.

Handles locating wallpaper directories, selecting random images,
and applying them as the Windows desktop wallpaper via ctypes.
"""

import ctypes
import logging
import random
from pathlib import Path

from config import SUPPORTED_EXTENSIONS, WALLPAPER_DIR

logger = logging.getLogger("MoodWallpaper")

# Windows API constants
SPI_SETDESKWALLPAPER: int = 0x0014
SPIF_UPDATEINIFILE: int = 0x01
SPIF_SENDCHANGE: int = 0x02


def get_wallpaper_path(emotion: str) -> Path | None:
    """Select a random wallpaper image for the given emotion.

    Looks inside the emotion-specific subdirectory under the
    configured wallpaper root and picks one file at random.

    Args:
        emotion: The detected emotion (e.g., "happy", "sad").

    Returns:
        Absolute Path to the selected wallpaper, or None on failure.
    """
    try:
        emotion_dir: Path = WALLPAPER_DIR / emotion.lower()

        if not emotion_dir.exists():
            logger.error("Wallpaper directory not found: %s", emotion_dir)
            return None

        if not emotion_dir.is_dir():
            logger.error("Wallpaper path is not a directory: %s", emotion_dir)
            return None

        # Collect images with supported extensions
        images: list[Path] = [
            f
            for f in emotion_dir.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
        ]

        if not images:
            logger.error("No wallpaper images found in: %s", emotion_dir)
            return None

        selected: Path = random.choice(images)
        logger.info("Wallpaper selected: %s", selected.name)

        return selected.resolve()

    except PermissionError as e:
        logger.error("Permission denied accessing wallpaper directory: %s", e)
        return None

    except Exception as e:
        logger.error("Error selecting wallpaper: %s", e)
        return None


def set_wallpaper(image_path: Path) -> bool:
    """Apply the given image as the Windows desktop wallpaper.

    Uses the Windows API SystemParametersInfoW to update the
    wallpaper and persist the change across sessions.

    Args:
        image_path: Absolute path to the wallpaper image file.

    Returns:
        True if the wallpaper was updated successfully, False otherwise.
    """
    try:
        if not image_path.exists():
            logger.error("Wallpaper file does not exist: %s", image_path)
            return False

        absolute_path: str = str(image_path.resolve())

        result: int = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            absolute_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
        )

        if result:
            logger.info("Wallpaper updated successfully to: %s", absolute_path)
            return True

        logger.error("SystemParametersInfoW returned failure.")
        return False

    except PermissionError as e:
        logger.error("Permission denied setting wallpaper: %s", e)
        return False

    except OSError as e:
        logger.error("OS error setting wallpaper: %s", e)
        return False

    except Exception as e:
        logger.error("Unexpected error setting wallpaper: %s", e)
        return False
