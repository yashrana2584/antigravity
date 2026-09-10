import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")

# File Paths
CASCADE_PATH = os.path.join(ASSETS_DIR, "haarcascade_frontalface_default.xml")
MODEL_PATH = os.path.join(MODEL_DIR, "face_recognizer.yml")
USERS_PATH = os.path.join(MODEL_DIR, "users.json")
CONFIG_PATH = os.path.join(MODEL_DIR, "config.json")

# Ensure required folders exist
for d in [ASSETS_DIR, DATA_DIR, MODEL_DIR]:
    os.makedirs(d, exist_ok=True)

# Face Recognition Parameters
# For OpenCV LBPH: confidence represents distance (lower = better match).
# Distances: < 50 is very high match, 50-78 is a valid match, > 80 is unknown.
CONFIDENCE_THRESHOLD = 78.0
REQUIRED_CONSECUTIVE_RECOGNITIONS = 3  # Number of matching frames needed to unlock
SAMPLE_COUNT_PER_USER = 35           # Number of face crops collected during enrollment

# Camera Configuration
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
FPS_TARGET = 30

# Voice & Speech Settings
VOICE_RATE = 175        # Words per minute
VOICE_VOLUME = 1.0      # 0.0 to 1.0
GREETING_TEMPLATE = "Welcome, {name}!"
UNLOCK_MESSAGE = "Access granted."
REGISTRATION_MESSAGE = "Welcome {name}! Your face has been successfully registered."

# Security & Master Fallback
DEFAULT_PIN = "1234"
COOLDOWN_AFTER_SPEECH = 2.0  # Seconds before repeating speech
