"""
mood_response.py - Therapeutic mood response module.

Maps each detected emotion to its therapeutic goal and a
set of encouraging messages. Logs one random message per run.

Emotion -> Goal -> Response logic:
  Happy   -> Maintain happiness   -> Encourage positivity
  Sad     -> Improve mood         -> Comfort and encourage
  Angry   -> Calm the user        -> Relaxation and stress relief
  Fear    -> Reduce anxiety       -> Reassurance and safety
  Surprise-> Maintain engagement  -> Positive acknowledgement
  Disgust -> Shift attention      -> Redirect to positive thoughts
  Neutral -> Maintain balance     -> Productive and balanced state
"""

import logging
import random

logger = logging.getLogger("MoodWallpaper")

# ── Therapeutic mapping ──────────────────────────────────────────────
# Structure: emotion -> { goal, wallpaper_theme, messages[] }
MOOD_RESPONSES: dict[str, dict] = {

    # HAPPY -> maintain happiness: vibrant sunflowers, golden meadows
    "happy": {
        "goal": "Maintain happiness",
        "theme": "Vibrant nature and joyful scenery",
        "messages": [
            "You're radiating happiness today! Keep spreading that positive energy.",
            "What a great mood! The world is brighter when you're smiling.",
            "Your happiness is contagious - enjoy every moment of this wonderful day!",
            "Feeling great? You deserve it! Keep that beautiful energy going.",
            "A happy you makes everything better. Enjoy your day to the fullest!",
        ],
    },

    # SAD -> improve mood: uplifting sunrise, rainbow, spring blossoms
    "sad": {
        "goal": "Improve mood",
        "theme": "Uplifting sunrise, rainbows and spring blossoms",
        "messages": [
            "Every storm runs out of rain. Brighter days are just ahead of you.",
            "It's okay to feel sad - but remember, you are stronger than you think.",
            "The sun always rises after the darkest night. You've got this!",
            "Take a deep breath. You are loved, valued, and better days are coming.",
            "Even the most beautiful flowers go through rain. Keep growing.",
        ],
    },

    # ANGRY -> calm the user: tranquil ocean, still lake, zen garden
    "angry": {
        "goal": "Calm the user",
        "theme": "Tranquil oceans, still lakes and zen gardens",
        "messages": [
            "Take a slow, deep breath. Let the calm ocean wash your stress away.",
            "Breathe in peace, breathe out tension. You are in control.",
            "Pause for a moment - still water runs deep. Let peace find you.",
            "Release what you cannot control. Focus on this moment of calm.",
            "Anger fades, but your inner peace is always there. Let it rise.",
        ],
    },

    # FEAR -> reduce anxiety: warm cozy cabin, safe meadow, gentle light
    "fear": {
        "goal": "Reduce anxiety",
        "theme": "Warm cozy lighting, safe meadows and gentle scenes",
        "messages": [
            "You are safe right now. Take a slow breath - everything is okay.",
            "Fear is just a feeling, not a fact. You are capable and protected.",
            "Breathe gently. You have overcome challenges before, and you will again.",
            "You are not alone. This moment will pass, and you will be just fine.",
            "Ground yourself - feel your feet on the floor. You are safe and secure.",
        ],
    },

    # SURPRISE -> maintain engagement: aurora, grand canyon, waterfall
    "surprise": {
        "goal": "Maintain engagement",
        "theme": "Stunning auroras, grand vistas and waterfalls",
        "messages": [
            "What a moment! Life is full of wonderful surprises - embrace this one.",
            "Surprise keeps life exciting! Stay curious and enjoy the ride.",
            "Something unexpected? The best stories often start that way!",
            "Life's surprises are what make it an adventure. Stay open to what's next.",
            "A surprised mind is an engaged mind - keep exploring!",
        ],
    },

    # DISGUST -> shift attention: fresh flowers, clear sky, crystal water
    "disgust": {
        "goal": "Shift attention",
        "theme": "Fresh flowers, clear blue skies and crystal water",
        "messages": [
            "Let's redirect your focus - notice the freshness and beauty around you.",
            "Shift your gaze to something pure and beautiful. The world has so much good.",
            "Take a breath of fresh air - clear your mind and find the good nearby.",
            "Focus on what uplifts you. Clean thoughts bring a clear mind.",
            "Move your attention to something that brings you joy - it's always there.",
        ],
    },

    # NEUTRAL -> maintain balance: mountain landscape, forest path
    "neutral": {
        "goal": "Maintain balance",
        "theme": "Balanced mountain landscapes and forest paths",
        "messages": [
            "You're in a steady, balanced state - a great foundation for a productive day.",
            "Calm and centred - you're right where you need to be. Keep going!",
            "Balance is the key to clarity. Use this moment to focus and create.",
            "A neutral mind is a ready mind. What great thing will you accomplish today?",
            "Steady and grounded - you have everything you need for a great day ahead.",
        ],
    },
}


def get_mood_response(emotion: str) -> dict:
    """Return the therapeutic goal, theme, and a random message for the emotion.

    Args:
        emotion: Detected emotion string (lowercase).

    Returns:
        Dict with keys: goal, theme, message.
    """
    emotion = emotion.lower().strip()
    data = MOOD_RESPONSES.get(emotion, MOOD_RESPONSES["neutral"])

    return {
        "goal": data["goal"],
        "theme": data["theme"],
        "message": random.choice(data["messages"]),
    }


def log_mood_response(emotion: str) -> None:
    """Log the therapeutic goal and message for the detected emotion.

    Args:
        emotion: Detected emotion string (lowercase).
    """
    response = get_mood_response(emotion)

    logger.info("-" * 50)
    logger.info("[EMOTION]  Detected    : %s", emotion.upper())
    logger.info("[GOAL]     Therapeutic : %s", response["goal"])
    logger.info("[THEME]    Wallpaper   : %s", response["theme"])
    logger.info("[MESSAGE]  %s", response["message"])
    logger.info("-" * 50)
