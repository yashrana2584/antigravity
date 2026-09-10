import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import time
import math
import config
from voice_engine import voice
from ui_draw import draw_hud_box, draw_scan_line

class LockScreenFrame(ctk.CTkFrame):
    def __init__(self, master, face_engine, on_unlock_callback, on_open_enroll_callback):
        super().__init__(master, fg_color="#0d0e15")
        self.master = master
        self.face_engine = face_engine
        self.on_unlock_callback = on_unlock_callback
        self.on_open_enroll_callback = on_open_enroll_callback

        self.cap = None
        self.is_active = False
        self.is_unlocked = False

        # Biometric state tracking
        self.consecutive_matches = 0
        self.last_matched_user = None
        self.scan_pos = 0.0
        self.scan_dir = 1

        self._build_ui()

    def _build_ui(self):
        # Top Clock and Date
        self.time_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.time_frame.pack(pady=(25, 10))

        self.clock_label = ctk.CTkLabel(
            self.time_frame,
            text="12:00:00 AM",
            font=ctk.CTkFont(size=52, weight="bold"),
            text_color="#ffffff"
        )
        self.clock_label.pack()

        self.date_label = ctk.CTkLabel(
            self.time_frame,
            text="Thursday, September 10, 2026",
            font=ctk.CTkFont(size=16),
            text_color="#888899"
        )
        self.date_label.pack()

        # Biometric Status Card
        self.card_frame = ctk.CTkFrame(self, fg_color="#151722", corner_radius=16, border_width=1, border_color="#2b2e3f")
        self.card_frame.pack(pady=10, padx=20)

        # Card Title
        self.header_row = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        self.header_row.pack(fill="x", padx=20, pady=(12, 6))

        self.lock_icon_label = ctk.CTkLabel(
            self.header_row,
            text="🔒 FACE BIOMETRIC LOCK",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#38ef7d"
        )
        self.lock_icon_label.pack(side="left")

        # Camera viewport
        self.cam_container = ctk.CTkFrame(self.card_frame, width=560, height=315, fg_color="#000000", corner_radius=10)
        self.cam_container.pack(padx=20, pady=10)
        self.cam_container.pack_propagate(False)

        self.cam_label = ctk.CTkLabel(self.cam_container, text="Initializing Biometric Camera...", text_color="#666677")
        self.cam_label.pack(expand=True, fill="both")

        # Status badge below camera
        self.status_badge = ctk.CTkLabel(
            self.card_frame,
            text="👁️ Looking for authorized face...",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#00d2d3"
        )
        self.status_badge.pack(pady=(5, 15))

        # Bottom Actions / Fallbacks
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(pady=(10, 20))

        self.pin_btn = ctk.CTkButton(
            self.actions_frame,
            text="🔑 Unlock with PIN",
            command=self._show_pin_dialog,
            fg_color="#232736",
            hover_color="#30354a",
            width=160
        )
        self.pin_btn.pack(side="left", padx=10)

        self.enroll_btn = ctk.CTkButton(
            self.actions_frame,
            text="👤 Face Enrollment",
            command=self.on_open_enroll_callback,
            fg_color="#232736",
            hover_color="#30354a",
            width=160
        )
        self.enroll_btn.pack(side="left", padx=10)

    def start_lock(self):
        """Activates the lock screen and camera loop."""
        self.is_active = True
        self.is_unlocked = False
        self.recent_matches = []
        self.last_matched_user = None

        # Always reload the latest users and model
        self.face_engine._load_users()
        self.face_engine._load_model()

        self.lock_icon_label.configure(text="🔒 FACE BIOMETRIC LOCK", text_color="#38ef7d")
        self.status_badge.configure(text="👁️ Looking for authorized face...", text_color="#00d2d3")

        # Open camera
        try:
            self.cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        except Exception as e:
            self.status_badge.configure(text=f"Camera error: {e}", text_color="#ff4757")
            return

        self._update_clock()
        self._camera_loop()

    def stop_lock(self):
        """Deactivates lock screen and releases camera."""
        self.is_active = False
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    def _update_clock(self):
        if not self.is_active:
            return
        now = time.localtime()
        time_str = time.strftime("%I:%M:%S %p", now)
        date_str = time.strftime("%A, %B %d, %Y", now)
        self.clock_label.configure(text=time_str)
        self.date_label.configure(text=date_str)
        self.after(500, self._update_clock)

    def _camera_loop(self):
        if not self.is_active or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.after(30, self._camera_loop)
            return

        # Flip horizontally for natural mirror feel
        frame = cv2.flip(frame, 1)

        # Animate scanline
        self.scan_pos += 0.02 * self.scan_dir
        if self.scan_pos >= 1.0:
            self.scan_pos = 1.0
            self.scan_dir = -1
        elif self.scan_pos <= 0.0:
            self.scan_pos = 0.0
            self.scan_dir = 1
        draw_scan_line(frame, self.scan_pos, color=(0, 200, 255))

        # Face detection
        faces = self.face_engine.detect_faces(frame)

        if not self.face_engine.has_registered_users():
            self.status_badge.configure(
                text="⚠️ No registered face profiles found! Click 'Face Enrollment' below.",
                text_color="#ffa502"
            )
            for (x, y, w, h) in faces:
                draw_hud_box(frame, x, y, w, h, color=(200, 200, 0), label="Unregistered", thickness=2)
        elif len(faces) == 0:
            if hasattr(self, 'recent_matches'):
                self.recent_matches.clear()
            self.status_badge.configure(text="👁️ Looking for authorized face...", text_color="#00d2d3")
        else:
            # Process largest face
            (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])
            face_crop = frame[y:y+h, x:x+w]

            if face_crop.size > 0:
                is_match, uid, name, conf_pct, dist = self.face_engine.recognize_face(face_crop)

                if is_match:
                    box_color = (0, 230, 80)  # Green
                    draw_hud_box(frame, x, y, w, h, color=box_color, label=name, confidence=conf_pct, thickness=2)

                    if not hasattr(self, 'recent_matches'):
                        self.recent_matches = []
                    self.recent_matches.append(name)
                    if len(self.recent_matches) > 5:
                        self.recent_matches.pop(0)

                    match_count = self.recent_matches.count(name)
                    self.status_badge.configure(
                        text=f"Verifying {name}... ({match_count}/{config.REQUIRED_CONSECUTIVE_RECOGNITIONS})",
                        text_color="#2ed573"
                    )

                    # Trigger unlock when required matches are satisfied
                    if match_count >= config.REQUIRED_CONSECUTIVE_RECOGNITIONS and not self.is_unlocked:
                        self.is_unlocked = True
                        self._trigger_unlock_sequence(name)
                        return
                else:
                    if hasattr(self, 'recent_matches') and len(self.recent_matches) > 0:
                        self.recent_matches.pop(0)
                    box_color = (0, 80, 255)  # Orange / Red
                    draw_hud_box(frame, x, y, w, h, color=box_color, label="Unknown Face", thickness=2)
                    self.status_badge.configure(
                        text="⚠️ Unknown Face Detected. Access Denied.",
                        text_color="#ff4757"
                    )

        # Render frame
        display_frame = cv2.resize(frame, (540, 304))
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(display_frame)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(540, 304))
        self.cam_label.configure(image=ctk_img, text="")

        self.after(25, self._camera_loop)

    def _trigger_unlock_sequence(self, user_name: str):
        """Displays celebration / unlock animation and speaks greeting."""
        self.lock_icon_label.configure(text=f"🔓 ACCESS GRANTED — WELCOME {user_name.upper()}", text_color="#2ed573")
        self.status_badge.configure(
            text=f"🎉 Recognized: {user_name}! Unlocking...",
            text_color="#2ed573"
        )

        # Voice Greeting: Always speaks "Welcome, <Name>! Access granted."
        voice.speak_welcome(user_name)

        # Stop camera and transition to unlocked dashboard
        self.after(1600, lambda: self._complete_unlock(user_name))

    def _complete_unlock(self, user_name: str):
        self.stop_lock()
        self.on_unlock_callback(user_name)

    def _show_pin_dialog(self):
        """Opens PIN fallback unlock prompt."""
        dialog = ctk.CTkInputDialog(text="Enter your 4-digit PIN (Default: 1234):", title="Security PIN Verification")
        pin = dialog.get_input()
        if pin:
            verified, name = self.face_engine.verify_pin(pin.strip())
            if verified:
                self.is_unlocked = True
                self._trigger_unlock_sequence(name)
            else:
                self.status_badge.configure(text="❌ Invalid PIN entered!", text_color="#ff4757")
