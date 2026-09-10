import customtkinter as ctk
import sys
import os

# Set appearance and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

import config
from face_engine import FaceEngine
from voice_engine import voice
from ui_lock_screen import LockScreenFrame
from ui_dashboard import DashboardFrame
from ui_enroll import EnrollWindow

class FaceUnlockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Face Biometric Unlock Screen")
        self.geometry("960x720")
        self.minsize(800, 600)

        # Center window on screen
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = max(0, (sw - 960) // 2)
        y = max(0, (sh - 720) // 2)
        self.geometry(f"960x720+{x}+{y}")

        self.is_fullscreen = False
        self.face_engine = FaceEngine()

        # Keyboard shortcuts
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._on_escape)

        # Container for views
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        # View frames
        self.lock_frame = LockScreenFrame(
            self.container,
            face_engine=self.face_engine,
            on_unlock_callback=self._on_unlock,
            on_open_enroll_callback=self._open_enrollment
        )

        self.dashboard_frame = DashboardFrame(
            self.container,
            face_engine=self.face_engine,
            on_relock_callback=self._relock,
            on_open_enroll_callback=self._open_enrollment
        )

        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        # Start on Lock Screen
        self._show_lock_screen()

        # If no users registered yet, prompt to enroll after a brief delay
        if not self.face_engine.has_registered_users():
            self.after(600, self._open_enrollment)

    def _show_lock_screen(self):
        self.dashboard_frame.pack_forget()
        self.lock_frame.pack(fill="both", expand=True)
        self.lock_frame.start_lock()

    def _on_unlock(self, user_name: str):
        self.lock_frame.stop_lock()
        self.lock_frame.pack_forget()
        self.dashboard_frame.set_user(user_name)
        self.dashboard_frame.pack(fill="both", expand=True)

    def _relock(self):
        voice.reset_cooldown()
        self._show_lock_screen()

    def _open_enrollment(self):
        # Temporarily stop camera in lock screen if active
        self.lock_frame.stop_lock()
        enroll_win = EnrollWindow(self, self.face_engine, on_complete_callback=self._on_enrollment_complete)
        enroll_win.grab_set()

    def _on_enrollment_complete(self):
        # Reload models and restart lock screen
        self.face_engine._load_users()
        self.face_engine._load_model()
        self._relock()

    def _toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def _on_escape(self, event=None):
        if self.is_fullscreen:
            self._toggle_fullscreen()

    def _on_exit(self):
        self.lock_frame.stop_lock()
        self.destroy()
        sys.exit(0)

if __name__ == "__main__":
    app = FaceUnlockApp()
    app.mainloop()
