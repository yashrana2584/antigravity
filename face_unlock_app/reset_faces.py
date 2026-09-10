import os
import sys
import glob

import config
from face_engine import FaceEngine

def reset_faces():
    print("=" * 60)
    print("      Face Biometric Unlock - Face Data Cleaner")
    print("=" * 60)

    engine = FaceEngine()
    users = engine.get_users_list()

    if not users:
        print("\nNo registered faces found to delete.")
        return

    print(f"\nFound {len(users)} registered user profile(s):")
    for u in users:
        print(f" - [{u['id']}] {u['name']} (Registered: {u.get('created_at', 'N/A')})")

    confirm = input("\nAre you sure you want to delete ALL face profiles and samples? (y/n): ").strip().lower()
    if confirm in ['y', 'yes']:
        success, msg = engine.reset_all_faces()
        print(f"\n✔ Result: {msg}")
    else:
        print("\nOperation cancelled. No faces were deleted.")

if __name__ == "__main__":
    reset_faces()
