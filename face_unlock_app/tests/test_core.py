import unittest
import numpy as np
import os
import sys

# Ensure app root is on path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import config
from face_engine import FaceEngine
from voice_engine import VoiceEngine

class TestCoreModules(unittest.TestCase):
    def test_cascade_exists(self):
        self.assertTrue(os.path.exists(config.CASCADE_PATH), "Cascade file must exist in assets")

    def test_face_engine_initialization(self):
        engine = FaceEngine()
        self.assertIsNotNone(engine.cascade, "Cascade classifier should be loaded")
        self.assertFalse(engine.cascade.empty(), "Cascade classifier should not be empty")

    def test_face_preprocess(self):
        engine = FaceEngine()
        # Create a dummy 100x100 BGR face image
        dummy_face = np.ones((100, 100, 3), dtype=np.uint8) * 128
        processed = engine.preprocess_face(dummy_face)
        self.assertEqual(processed.shape, (200, 200), "Preprocessed face should be 200x200")
        self.assertEqual(len(processed.shape), 2, "Preprocessed face should be single-channel grayscale")

    def test_synthetic_training_and_recognition(self):
        engine = FaceEngine()
        # Register a test synthetic user
        test_uid = "9999"
        engine.users[test_uid] = {"id": test_uid, "name": "SyntheticTester", "pin": "9999"}

        # Create 5 synthetic face patterns
        synthetic_samples = []
        for i in range(5):
            arr = np.full((200, 200), 100 + i * 5, dtype=np.uint8)
            # draw simple shape
            arr[50:150, 50:150] = 200
            synthetic_samples.append(arr)
            engine.save_sample_crop(test_uid, i, arr)

        # Train model
        success, msg = engine.train_model()
        self.assertTrue(success, f"Training failed: {msg}")
        self.assertTrue(engine.model_loaded, "Model should be loaded after training")

        # Test recognition on sample
        matched, uid, name, conf_pct, dist = engine.recognize_face(synthetic_samples[0])
        self.assertTrue(matched, f"Synthetic face should match, distance: {dist}")
        self.assertEqual(name, "SyntheticTester")

        # Clean up synthetic sample files
        for i in range(5):
            p = os.path.join(config.DATA_DIR, f"user_{test_uid}_sample_{i:03d}.png")
            if os.path.exists(p):
                os.remove(p)
        del engine.users[test_uid]
        engine._save_users()

    def test_voice_engine_singleton(self):
        v1 = VoiceEngine()
        v2 = VoiceEngine()
        self.assertIs(v1, v2, "VoiceEngine must be a singleton")

    def test_delete_and_reset(self):
        engine = FaceEngine()
        u_id = engine.register_new_user("DeleteMeUser", "1234")
        self.assertIn(u_id, engine.users)

        # Save dummy sample
        dummy = np.zeros((200, 200), dtype=np.uint8)
        engine.save_sample_crop(u_id, 0, dummy)

        # Delete single user
        ok, msg = engine.delete_user(u_id)
        self.assertTrue(ok)
        self.assertNotIn(u_id, engine.users)

        # Reset all
        ok, msg = engine.reset_all_faces()
        self.assertTrue(ok)
        self.assertEqual(len(engine.users), 0)

if __name__ == "__main__":
    unittest.main()
