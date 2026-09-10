import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import time
import threading
import config
from voice_engine import voice
from ui_draw import draw_hud_box

class EnrollWindow(ctk.CTkToplevel):
    def __init__(self, master, face_engine, on_complete_callback=None):
        super().__init__(master)
        self.master = master
        self.face_engine = face_engine
        self.on_complete_callback = on_complete_callback

        self.title("Face Biometric Enrollment Wizard")
        self.geometry("780x680")
        self.resizable(False, False)

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 780) // 2
        y = (self.winfo_screenheight() - 680) // 2
        self.geometry(f"+{x}+{y}")

        self.cap = None
        self.is_capturing = False
        self.samples_collected = 0
        self.target_samples = config.SAMPLE_COUNT_PER_USER
        self.current_user_id = None
        self.current_user_name = ""
        self.last_capture_time = 0.0
        self.is_training = False

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Biometric Face Enrollment",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.pack(anchor="w")

        self.sub_label = ctk.CTkLabel(
            self.header_frame,
            text="Register your face so the lock screen can recognize you and greet you by name.",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.sub_label.pack(anchor="w")

        # Form Inputs (Name & PIN)
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="x", padx=20, pady=10)

        # Name Entry
        ctk.CTkLabel(self.form_frame, text="Your Name:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=15, pady=10, sticky="w")
        self.name_entry = ctk.CTkEntry(self.form_frame, placeholder_text="e.g. Alex", width=220)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Backup PIN Entry
        ctk.CTkLabel(self.form_frame, text="Backup PIN:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=2, padx=15, pady=10, sticky="w")
        self.pin_entry = ctk.CTkEntry(self.form_frame, placeholder_text="1234", width=120, show="*")
        self.pin_entry.insert(0, "1234")
        self.pin_entry.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Start Capture Button
        self.start_btn = ctk.CTkButton(
            self.form_frame,
            text="▶ Start Face Scan",
            command=self._start_capture,
            fg_color="#1f6aa5",
            hover_color="#144870",
            font=ctk.CTkFont(weight="bold")
        )
        self.start_btn.grid(row=0, column=4, padx=15, pady=10)

        # Camera Viewport
        self.cam_frame = ctk.CTkFrame(self, width=640, height=360, fg_color="#111116", corner_radius=10)
        self.cam_frame.pack(padx=20, pady=10)
        self.cam_frame.pack_propagate(False)

        self.cam_label = ctk.CTkLabel(self.cam_frame, text="Camera Preview (Press Start)", text_color="gray")
        self.cam_label.pack(expand=True, fill="both")

        # Progress bar and instructions
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=20, pady=5)

        self.status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Ready. Enter your name and click 'Start Face Scan'.",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.status_label.pack(pady=(5, 5))

        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=500)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(pady=5)

        self.count_label = ctk.CTkLabel(
            self.progress_frame,
            text="0 / 35 Samples Captured",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.count_label.pack()

        # Bottom Buttons
        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", padx=20, pady=(10, 15))

        self.close_btn = ctk.CTkButton(
            self.bottom_frame,
            text="Cancel & Return",
            fg_color="#444444",
            hover_color="#333333",
            command=self._on_close
        )
        self.close_btn.pack(side="right", padx=10)

    def _start_capture(self):
        name = self.name_entry.get().strip()
        if not name:
            self.status_label.configure(text="⚠️ Please enter your name first!", text_color="#ff4757")
            return

        pin = self.pin_entry.get().strip() or "1234"
        self.current_user_name = name
        self.current_user_id = self.face_engine.register_new_user(name, pin)
        self.samples_collected = 0
        self.is_capturing = True

        # Disable form controls
        self.name_entry.configure(state="disabled")
        self.pin_entry.configure(state="disabled")
        self.start_btn.configure(state="disabled")

        self.status_label.configure(text="Initializing camera... please look directly at the webcam.", text_color="#2ed573")

        # Open camera
        try:
            self.cap = cv2.VideoCapture(config.CAMERA_INDEX, cv2.CAP_DSHOW)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        except Exception as e:
            self.status_label.configure(text=f"Camera error: {e}", text_color="#ff4757")
            return

        self._video_loop()

    def _video_loop(self):
        if not self.is_capturing or self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.after(30, self._video_loop)
            return

        # Flip horizontally for natural mirror effect
        frame = cv2.flip(frame, 1)
        faces = self.face_engine.detect_faces(frame)

        now = time.time()
        # Collect sample every 120ms if face is detected
        if len(faces) > 0 and (now - self.last_capture_time) > 0.12 and self.samples_collected < self.target_samples:
            # Pick largest detected face
            (x, y, w, h) = max(faces, key=lambda b: b[2] * b[3])
            face_crop = frame[y:y+h, x:x+w]
            if face_crop.size > 0:
                self.face_engine.save_sample_crop(self.current_user_id, self.samples_collected, face_crop)
                self.samples_collected += 1
                self.last_capture_time = now

                # Update UI progress
                progress = self.samples_collected / self.target_samples
                self.progress_bar.set(progress)
                self.count_label.configure(text=f"{self.samples_collected} / {self.target_samples} Samples Captured")

                # Dynamic feedback
                if self.samples_collected < 12:
                    self.status_label.configure(text="Looking good! Please look straight at the camera.", text_color="#00d2d3")
                elif self.samples_collected < 24:
                    self.status_label.configure(text="Great! Now tilt your head slightly left and right.", text_color="#10ac84")
                else:
                    self.status_label.configure(text="Almost done! Smile or alter your expression slightly.", text_color="#2ed573")

        # Draw HUD brackets on detected faces
        for (x, y, w, h) in faces:
            draw_hud_box(frame, x, y, w, h, color=(0, 230, 80), label=self.current_user_name, thickness=2)

        # Check if collection is complete
        if self.samples_collected >= self.target_samples:
            self.is_capturing = False
            self._release_camera()
            self._finalize_training()
            return

        # Render frame in CTkLabel
        display_frame = cv2.resize(frame, (600, 340))
        display_frame = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(display_frame)
        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(600, 340))
        self.cam_label.configure(image=ctk_img, text="")

        self.after(25, self._video_loop)

    def _finalize_training(self):
        self.status_label.configure(text="Training facial recognition neural model... Please wait a moment.", text_color="#ffa502")
        self.progress_bar.set(1.0)
        self.update()

        def train_task():
            success, msg = self.face_engine.train_model()
            self.after(0, lambda: self._on_training_finished(success, msg))

        threading.Thread(target=train_task, daemon=True).start()

    def _on_training_finished(self, success: bool, msg: str):
        if success:
            self._training_completed = True
            self.status_label.configure(
                text=f"🎉 Registration Complete! Welcome, {self.current_user_name}.",
                text_color="#2ed573"
            )
            # Audible voice confirmation
            voice.speak_registration_success(self.current_user_name)

            self.close_btn.configure(
                text="✔ Done - Go to Lock Screen",
                fg_color="#2ed573",
                hover_color="#26af5f",
                command=self._on_done_and_close
            )
        else:
            self._training_completed = False
            self.status_label.configure(text=f"Training error: {msg}", text_color="#ff4757")
            self.close_btn.configure(text="Close", command=self._on_close)

    def _on_done_and_close(self):
        self._on_close()

    def _release_camera(self):
        if self.cap is not None:
            try:
                self.cap.release()
            except Exception:
                pass
            self.cap = None

    def _on_close(self):
        self.is_capturing = False
        self._release_camera()
        self.destroy()
        if getattr(self, '_training_completed', False):
            if self.on_complete_callback:
                self.on_complete_callback()
