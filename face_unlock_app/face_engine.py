import os
import json
import cv2
import numpy as np
import time
import logging
import config

logger = logging.getLogger(__name__)

class FaceEngine:
    def __init__(self):
        self.cascade = None
        self.recognizer = None
        self.users = {}
        self.model_loaded = False
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

        self._load_cascade()
        self._load_users()
        self._load_model()

    def _load_cascade(self):
        """Loads the Haar Cascade face detector."""
        if not os.path.exists(config.CASCADE_PATH):
            raise FileNotFoundError(f"Haar cascade XML not found at {config.CASCADE_PATH}")
        self.cascade = cv2.CascadeClassifier(config.CASCADE_PATH)
        if self.cascade.empty():
            raise RuntimeError(f"Failed to load cascade classifier from {config.CASCADE_PATH}")

    def _load_users(self):
        """Loads registered users from JSON."""
        if os.path.exists(config.USERS_PATH):
            try:
                with open(config.USERS_PATH, "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except Exception as e:
                logger.error(f"Failed to read users file: {e}")
                self.users = {}
        else:
            self.users = {}

    def _save_users(self):
        """Saves registered users to JSON."""
        try:
            with open(config.USERS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.users, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save users file: {e}")

    def _load_model(self):
        """Loads trained LBPH model if available."""
        if hasattr(cv2, 'face') and os.path.exists(config.MODEL_PATH) and len(self.users) > 0:
            try:
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read(config.MODEL_PATH)
                self.model_loaded = True
                logger.info("LBPH Face Recognizer loaded successfully.")
            except Exception as e:
                logger.error(f"Error loading trained model: {e}")
                self.model_loaded = False
        else:
            self.model_loaded = False

    def has_registered_users(self) -> bool:
        return len(self.users) > 0 and self.model_loaded

    def get_users_list(self) -> list:
        return list(self.users.values())

    def preprocess_face(self, face_img: np.ndarray) -> np.ndarray:
        """Grayscale, standard resize (200x200), and CLAHE contrast equalization."""
        if len(face_img.shape) == 3:
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = face_img
        resized = cv2.resize(gray, (200, 200), interpolation=cv2.INTER_CUBIC)
        equalized = self.clahe.apply(resized)
        return equalized

    def detect_faces(self, frame_bgr: np.ndarray):
        """
        Detects faces in BGR image.
        Returns list of bounding boxes: [(x, y, w, h), ...]
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=1.15,
            minNeighbors=5,
            minSize=(80, 80),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces

    def register_new_user(self, name: str, pin: str = "1234") -> str:
        """Allocates a new user ID and saves metadata."""
        # Find next numeric ID
        existing_ids = [int(k) for k in self.users.keys()] if self.users else [0]
        next_id = str(max(existing_ids) + 1 if existing_ids else 1)
        self.users[next_id] = {
            "id": next_id,
            "name": name.strip(),
            "pin": pin.strip() if pin else config.DEFAULT_PIN,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._save_users()
        return next_id

    def save_sample_crop(self, user_id: str, sample_index: int, face_crop: np.ndarray):
        """Saves a normalized face crop for model training."""
        processed = self.preprocess_face(face_crop)
        filename = f"user_{user_id}_sample_{sample_index:03d}.png"
        filepath = os.path.join(config.DATA_DIR, filename)
        cv2.imwrite(filepath, processed)

    def train_model(self) -> tuple[bool, str]:
        """
        Trains the LBPH face recognizer from all sample images in DATA_DIR.
        Returns (success, message).
        """
        if not hasattr(cv2, 'face'):
            return False, "OpenCV face module not available."

        images = []
        labels = []

        for fname in os.listdir(config.DATA_DIR):
            if fname.endswith(".png") and fname.startswith("user_"):
                parts = fname.split("_")
                if len(parts) >= 4:
                    try:
                        u_id = int(parts[1])
                        img_path = os.path.join(config.DATA_DIR, fname)
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                        if img is not None:
                            images.append(img)
                            labels.append(u_id)
                    except ValueError:
                        continue

        if not images:
            return False, "No face samples found to train."

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create(radius=1, neighbors=8, grid_x=8, grid_y=8)
            recognizer.train(images, np.array(labels))
            recognizer.write(config.MODEL_PATH)
            self.recognizer = recognizer
            self.model_loaded = True
            logger.info(f"Successfully trained LBPH model on {len(images)} samples across {len(set(labels))} users.")
            return True, f"Trained successfully on {len(images)} samples!"
        except Exception as e:
            logger.error(f"Training failed: {e}")
            return False, str(e)

    def recognize_face(self, face_bgr: np.ndarray):
        """
        Recognizes a face crop.
        Returns:
            matched (bool): True if recognized with confidence < threshold
            user_id (str or None): ID of recognized user
            user_name (str): Name of user, or 'Unknown'
            confidence_pct (int): 0-100% confidence estimate
            raw_distance (float): LBPH distance
        """
        if not self.model_loaded or self.recognizer is None:
            return False, None, "Unconfigured", 0, 999.0

        processed = self.preprocess_face(face_bgr)
        try:
            label_id, distance = self.recognizer.predict(processed)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return False, None, "Error", 0, 999.0

        user_id_str = str(label_id)
        user_info = self.users.get(user_id_str)

        # Distance to Confidence Percentage mapping:
        # Distance = 0 -> 100% match
        # Distance = 50 -> 80% match
        # Distance = 70 -> 55% match
        # Distance > 80 -> < 40% match
        confidence_pct = max(0, min(100, int(100 - (distance / 80.0) * 60)))

        is_match = (distance <= config.CONFIDENCE_THRESHOLD) and (user_info is not None)
        user_name = user_info["name"] if is_match and user_info else "Unknown"

        return is_match, user_id_str if is_match else None, user_name, confidence_pct, distance

    def verify_pin(self, entered_pin: str) -> tuple[bool, str]:
        """Checks entered PIN against registered users or master PIN."""
        if entered_pin == config.DEFAULT_PIN:
            return True, "Master PIN"
        for uid, data in self.users.items():
            if data.get("pin") == entered_pin:
                return True, data.get("name", "User")
        return False, ""

    def delete_user(self, user_id: str) -> tuple[bool, str]:
        """Deletes all face samples for a specific user and retrains model."""
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            return False, f"User ID {user_id_str} not found."

        deleted_user_name = self.users[user_id_str].get("name", "User")
        del self.users[user_id_str]
        self._save_users()

        # Remove sample images
        prefix = f"user_{user_id_str}_"
        for fname in os.listdir(config.DATA_DIR):
            if fname.startswith(prefix) and fname.endswith(".png"):
                try:
                    os.remove(os.path.join(config.DATA_DIR, fname))
                except Exception as e:
                    logger.error(f"Error removing {fname}: {e}")

        # Retrain or reset model
        if len(self.users) > 0:
            self.train_model()
        else:
            if os.path.exists(config.MODEL_PATH):
                try:
                    os.remove(config.MODEL_PATH)
                except Exception:
                    pass
            self.recognizer = None
            self.model_loaded = False

        return True, f"Deleted user '{deleted_user_name}'."

    def reset_all_faces(self) -> tuple[bool, str]:
        """Deletes all registered faces, models, and user metadata."""
        # Remove all sample images
        for fname in os.listdir(config.DATA_DIR):
            if fname.endswith(".png"):
                try:
                    os.remove(os.path.join(config.DATA_DIR, fname))
                except Exception:
                    pass

        # Remove model and users json
        if os.path.exists(config.MODEL_PATH):
            try:
                os.remove(config.MODEL_PATH)
            except Exception:
                pass

        if os.path.exists(config.USERS_PATH):
            try:
                os.remove(config.USERS_PATH)
            except Exception:
                pass

        self.users = {}
        self.recognizer = None
        self.model_loaded = False
        return True, "All faces and user profiles have been deleted."
