import customtkinter as ctk
import time
import config
from voice_engine import voice

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, face_engine, on_relock_callback, on_open_enroll_callback):
        super().__init__(master, fg_color="#0e1117")
        self.master = master
        self.face_engine = face_engine
        self.on_relock_callback = on_relock_callback
        self.on_open_enroll_callback = on_open_enroll_callback

        self.current_user = "User"
        self._build_ui()

    def _build_ui(self):
        # Header banner
        self.header_frame = ctk.CTkFrame(self, fg_color="#181e29", corner_radius=16)
        self.header_frame.pack(fill="x", padx=30, pady=(30, 20))

        self.welcome_label = ctk.CTkLabel(
            self.header_frame,
            text="✨ Welcome Back!",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#38ef7d"
        )
        self.welcome_label.pack(anchor="w", padx=25, pady=(20, 5))

        self.status_sublabel = ctk.CTkLabel(
            self.header_frame,
            text="Face verification succeeded. Screen unlocked and secure session active.",
            font=ctk.CTkFont(size=14),
            text_color="#8892b0"
        )
        self.status_sublabel.pack(anchor="w", padx=25, pady=(0, 20))

        # Main Grid / Quick Actions
        self.actions_container = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_container.pack(fill="x", padx=30, pady=10)

        # Card 1: Re-Lock
        self.relock_card = ctk.CTkFrame(self.actions_container, fg_color="#161b26", corner_radius=14)
        self.relock_card.pack(side="left", expand=True, fill="both", padx=(0, 10), pady=5)

        ctk.CTkLabel(self.relock_card, text="🔒 Lock Screen", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(
            self.relock_card,
            text="Immediately return to the biometric lock screen to test facial unlock.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=220
        ).pack(anchor="w", padx=20, pady=(0, 15))

        self.relock_btn = ctk.CTkButton(
            self.relock_card,
            text="Lock Now",
            fg_color="#e74c3c",
            hover_color="#c0392b",
            font=ctk.CTkFont(weight="bold"),
            command=self.on_relock_callback
        )
        self.relock_btn.pack(padx=20, pady=(0, 15), fill="x")

        # Card 2: Face Enrollment
        self.enroll_card = ctk.CTkFrame(self.actions_container, fg_color="#161b26", corner_radius=14)
        self.enroll_card.pack(side="left", expand=True, fill="both", padx=10, pady=5)

        ctk.CTkLabel(self.enroll_card, text="👤 Face Profiles", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(
            self.enroll_card,
            text="Add another user profile or re-scan your face for higher accuracy.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=220
        ).pack(anchor="w", padx=20, pady=(0, 15))

        self.enroll_btn = ctk.CTkButton(
            self.enroll_card,
            text="Enroll Face",
            fg_color="#1f6aa5",
            hover_color="#144870",
            font=ctk.CTkFont(weight="bold"),
            command=self.on_open_enroll_callback
        )
        self.enroll_btn.pack(padx=20, pady=(0, 15), fill="x")

        # Card 3: Voice Test
        self.voice_card = ctk.CTkFrame(self.actions_container, fg_color="#161b26", corner_radius=14)
        self.voice_card.pack(side="left", expand=True, fill="both", padx=(10, 0), pady=5)

        ctk.CTkLabel(self.voice_card, text="🔊 Audio Greeting", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", padx=20, pady=(15, 5))
        ctk.CTkLabel(
            self.voice_card,
            text="Test your custom voice greeting through your speakers.",
            font=ctk.CTkFont(size=12),
            text_color="gray",
            wraplength=220
        ).pack(anchor="w", padx=20, pady=(0, 15))

        self.voice_btn = ctk.CTkButton(
            self.voice_card,
            text="Test Speech",
            fg_color="#2ed573",
            hover_color="#26af5f",
            font=ctk.CTkFont(weight="bold"),
            command=self._test_voice
        )
        self.voice_btn.pack(padx=20, pady=(0, 15), fill="x")

        # Settings & Profiles Info Frame
        self.info_frame = ctk.CTkFrame(self, fg_color="#161b26", corner_radius=14)
        self.info_frame.pack(fill="x", padx=30, pady=15)

        self.info_header = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.info_header.pack(fill="x", padx=20, pady=(15, 5))

        ctk.CTkLabel(self.info_header, text="⚙️ Enrolled Face Profiles & Settings", font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")

        self.reset_all_btn = ctk.CTkButton(
            self.info_header,
            text="🗑️ Reset All Faces",
            fg_color="#c0392b",
            hover_color="#962d22",
            font=ctk.CTkFont(size=12, weight="bold"),
            width=130,
            height=28,
            command=self._confirm_reset_all
        )
        self.reset_all_btn.pack(side="right")

        # Container for user list cards
        self.users_container = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.users_container.pack(fill="x", padx=20, pady=5)

        # Confidence Slider
        self.slider_row = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.slider_row.pack(fill="x", padx=20, pady=(10, 15))

        ctk.CTkLabel(self.slider_row, text="Recognition Threshold (Lower = Stricter):", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(0, 10))
        self.threshold_slider = ctk.CTkSlider(self.slider_row, from_=40, to=90, number_of_steps=50, command=self._on_threshold_change)
        self.threshold_slider.set(config.CONFIDENCE_THRESHOLD)
        self.threshold_slider.pack(side="left", fill="x", expand=True, padx=10)

        self.threshold_val_lbl = ctk.CTkLabel(self.slider_row, text=f"{int(config.CONFIDENCE_THRESHOLD)}")
        self.threshold_val_lbl.pack(side="left", padx=5)

    def set_user(self, user_name: str):
        self.current_user = user_name
        self.welcome_label.configure(text=f"✨ Welcome Back, {user_name}!")
        self._refresh_users_list()

    def _refresh_users_list(self):
        # Clear existing user rows
        for child in self.users_container.winfo_children():
            child.destroy()

        users = self.face_engine.get_users_list()
        if not users:
            ctk.CTkLabel(
                self.users_container,
                text="No faces currently registered. Click 'Enroll Face' above to register.",
                text_color="gray",
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", pady=5)
            self.reset_all_btn.configure(state="disabled")
            return

        self.reset_all_btn.configure(state="normal")
        for u in users:
            uid = str(u["id"])
            uname = u.get("name", "User")
            created = u.get("created_at", "")

            row = ctk.CTkFrame(self.users_container, fg_color="#1f2430", corner_radius=8)
            row.pack(fill="x", pady=3)

            info_text = f"👤 {uname} (ID: {uid})"
            if created:
                info_text += f"  •  Registered: {created}"

            ctk.CTkLabel(row, text=info_text, font=ctk.CTkFont(size=13, weight="bold"), text_color="#00d2d3").pack(side="left", padx=12, pady=8)

            del_btn = ctk.CTkButton(
                row,
                text="🗑️ Delete",
                width=80,
                height=26,
                fg_color="#802020",
                hover_color="#a02828",
                command=lambda target_id=uid, target_name=uname: self._confirm_delete_user(target_id, target_name)
            )
            del_btn.pack(side="right", padx=10, pady=6)

    def _confirm_delete_user(self, user_id: str, user_name: str):
        from tkinter import messagebox
        if messagebox.askyesno("Delete Face Profile", f"Are you sure you want to delete profile for '{user_name}'?"):
            success, msg = self.face_engine.delete_user(user_id)
            if success:
                messagebox.showinfo("Deleted", msg)
            else:
                messagebox.showerror("Error", msg)
            self._refresh_users_list()

    def _confirm_reset_all(self):
        from tkinter import messagebox
        if messagebox.askyesno("Reset All Faces", "Are you sure you want to delete ALL registered faces and reset the database? This cannot be undone."):
            success, msg = self.face_engine.reset_all_faces()
            messagebox.showinfo("Reset Complete", msg)
            self._refresh_users_list()

    def _test_voice(self):
        voice.reset_cooldown()
        voice.speak_greeting(self.current_user)

    def _on_threshold_change(self, val):
        config.CONFIDENCE_THRESHOLD = float(val)
        self.threshold_val_lbl.configure(text=f"{int(val)}")
