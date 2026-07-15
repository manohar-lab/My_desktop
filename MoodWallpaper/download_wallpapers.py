"""
download_wallpapers.py - Downloads open-source wallpapers from Unsplash
for each emotion's therapeutic goal.

Therapeutic wallpaper mapping:
  Happy   -> Maintain happiness   -> Vibrant cheerful nature
  Sad     -> Improve mood         -> Uplifting sunrise, rainbows, blossoms
  Angry   -> Calm the user        -> Tranquil ocean, still lake, zen garden
  Fear    -> Reduce anxiety       -> Warm cozy cabin, safe meadow
  Surprise-> Maintain engagement  -> Aurora, grand canyon, waterfall
  Disgust -> Shift attention      -> Fresh flowers, clear sky, clean water
  Neutral -> Maintain balance     -> Mountain landscape, forest path

Images sourced from Unsplash (free, open-source, no attribution required).
Uses the ?w=1920&q=85 query string for high resolution downloads.
"""

import sys
import time
from pathlib import Path

import requests

# Unsplash source URLs
# Format: https://images.unsplash.com/photo-<PHOTO_ID>?w=1920&q=80&fit=crop&auto=format
WALLPAPERS: dict[str, list[tuple[str, str]]] = {

    # HAPPY -> maintain happiness: bright sunflowers, golden meadows
    "happy": [
        (
            "happy_sunflower_field.jpg",
            "https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "happy_golden_poppy.jpg",
            "https://images.unsplash.com/photo-1560807707-8cc77767d783?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "happy_bright_forest.jpg",
            "https://images.unsplash.com/photo-1448375240586-882707db888b?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # SAD -> improve mood: uplifting sunrise, rainbow, spring blossoms
    "sad": [
        (
            "sad_uplift_sunrise.jpg",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "sad_uplift_spring_bloom.jpg",
            "https://images.unsplash.com/photo-1522748906645-95d8adfd52c7?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "sad_uplift_golden_light.jpg",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # ANGRY -> calm the user: tranquil ocean, still lake, zen garden
    "angry": [
        (
            "angry_calm_ocean.jpg",
            "https://images.unsplash.com/photo-1505118380757-91f5f5632de0?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "angry_calm_still_lake.jpg",
            "https://images.unsplash.com/photo-1482192505345-5852ba8f4f69?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "angry_calm_mountain_lake.jpg",
            "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # NEUTRAL -> maintain balance: clean landscape, forest path, desk
    "neutral": [
        (
            "neutral_mountain_path.jpg",
            "https://images.unsplash.com/photo-1434725039720-aaad6dd32dfe?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "neutral_forest_light.jpg",
            "https://images.unsplash.com/photo-1511497584788-876760111969?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "neutral_minimal_workspace.jpg",
            "https://images.unsplash.com/photo-1483058712412-4245e9b90334?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # FEAR -> reduce anxiety: warm cozy lighting, safe meadow, gentle nature
    "fear": [
        (
            "fear_safe_cozy_light.jpg",
            "https://images.unsplash.com/photo-1476611338391-6f395a0ebc7b?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "fear_safe_gentle_meadow.jpg",
            "https://images.unsplash.com/photo-1418065460487-3e41a6c84dc5?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "fear_safe_warm_sunset.jpg",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # SURPRISE -> maintain engagement: aurora, grand vista, waterfall
    "surprise": [
        (
            "surprise_aurora.jpg",
            "https://images.unsplash.com/photo-1531366936337-7c912a4589a7?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "surprise_waterfall.jpg",
            "https://images.unsplash.com/photo-1467890947394-8171244e5410?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "surprise_milky_way.jpg",
            "https://images.unsplash.com/photo-1537420327992-d6e192287183?w=1920&q=80&fit=crop&auto=format",
        ),
    ],

    # DISGUST -> shift attention: fresh flowers, clear blue sky, clean water
    "disgust": [
        (
            "disgust_fresh_lavender.jpg",
            "https://images.unsplash.com/photo-1499028344343-cd173ffc68a9?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "disgust_clear_sky.jpg",
            "https://images.unsplash.com/photo-1504701954957-2010ec3bcec1?w=1920&q=80&fit=crop&auto=format",
        ),
        (
            "disgust_crystal_stream.jpg",
            "https://images.unsplash.com/photo-1508739773434-c26b3d09e071?w=1920&q=80&fit=crop&auto=format",
        ),
    ],
}

WALLPAPER_BASE = Path(__file__).resolve().parent / "wallpapers"
HEADERS = {"User-Agent": "MoodWallpaper/1.0 (open-source project)"}


def download_file(url: str, dest: Path) -> bool:
    """Download a file from url to dest, return True on success."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except requests.HTTPError as e:
        print(f"    FAILED (HTTP {e.response.status_code}): {url}")
        return False
    except Exception as e:
        print(f"    FAILED: {e}")
        return False


def main() -> None:
    total = sum(len(v) for v in WALLPAPERS.values())
    done = 0
    failed = 0

    print()
    print("=" * 62)
    print("  Downloading open-source wallpapers from Unsplash")
    print(f"  Total images: {total}")
    print("=" * 62)

    for emotion, images in WALLPAPERS.items():
        folder = WALLPAPER_BASE / emotion
        folder.mkdir(parents=True, exist_ok=True)

        # Remove old wallpapers (AI-generated or previous downloads)
        removed = 0
        for old in folder.iterdir():
            if old.is_file():
                old.unlink()
                removed += 1
        if removed:
            print(f"\n  Cleared {removed} old file(s) from {emotion}/")

        print(f"\n[{emotion.upper()}]")
        for filename, url in images:
            dest = folder / filename
            print(f"  >> {filename} ...", end=" ", flush=True)
            if download_file(url, dest):
                size_kb = dest.stat().st_size // 1024
                print(f"OK ({size_kb} KB)")
                done += 1
            else:
                failed += 1
            time.sleep(0.4)  # polite rate limiting

    print()
    print("=" * 62)
    print(f"  Done: {done}/{total} downloaded  |  {failed} failed")
    print("=" * 62)
    print()

    if failed > 0:
        print(f"  WARNING: {failed} image(s) failed. Check URLs or network.")
        sys.exit(1)


if __name__ == "__main__":
    main()
