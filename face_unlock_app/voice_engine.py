import threading
import queue
import time
import winsound
import logging
import config

logger = logging.getLogger(__name__)

class VoiceEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(VoiceEngine, cls).__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.speech_queue = queue.Queue(maxsize=5)
        self.last_spoken_time = 0.0
        self.last_spoken_name = None
        self.is_speaking = False

        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()

    def _speech_worker(self):
        """Worker thread using Windows native SAPI with COM initialization."""
        speaker = None
        use_sapi = False

        try:
            import pythoncom
            import win32com.client
            pythoncom.CoInitialize()
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # SAPI Rate ranges from -10 to 10. 0 is normal speed.
            speaker.Rate = 0
            speaker.Volume = 100
            use_sapi = True
            logger.info("Windows native SAPI.SpVoice initialized successfully.")
        except Exception as e:
            logger.warning(f"Native SAPI init failed, falling back to pyttsx3/powershell: {e}")

        while True:
            try:
                task = self.speech_queue.get()
                if task is None:
                    break
                text, play_chime = task
                self.is_speaking = True

                if play_chime:
                    try:
                        winsound.MessageBeep(winsound.MB_ICONASTERISK)
                    except Exception:
                        pass

                spoken = False
                if use_sapi and speaker is not None:
                    try:
                        speaker.Speak(text)
                        spoken = True
                    except Exception as e:
                        logger.error(f"SAPI speak error: {e}")

                if not spoken:
                    # Secondary fallback: PowerShell Speech Synthesizer
                    self._powershell_fallback_speak(text)

                self.is_speaking = False
                self.speech_queue.task_done()
            except Exception as e:
                logger.error(f"Error in speech worker loop: {e}")
                self.is_speaking = False

    def _powershell_fallback_speak(self, text: str):
        """Fallback using Windows System.Speech."""
        try:
            import subprocess
            escaped = text.replace('"', '`"')
            cmd = f'Add-Type -AssemblyName System.Speech; $s = New-Object System.Speech.Synthesis.SpeechSynthesizer; $s.Rate = 0; $s.Speak("{escaped}")'
            subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, timeout=6)
        except Exception as e:
            logger.error(f"PowerShell TTS fallback error: {e}")

    def speak(self, text: str, play_chime: bool = False, force: bool = False):
        """Queues a message to be spoken. If force=True, clears queue backlog."""
        if not text:
            return

        if force:
            # Drain any old pending speech tasks
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                    self.speech_queue.task_done()
                except Exception:
                    break

        try:
            self.speech_queue.put_nowait((text, play_chime))
        except queue.Full:
            pass

    def speak_welcome(self, name: str) -> bool:
        """
        Speaks 'Welcome, <Name>! Access granted.'
        Always forces the speech output for unlocks.
        """
        now = time.time()
        # Allow greeting if name changed OR if cooldown passed
        if self.last_spoken_name == name and (now - self.last_spoken_time) < config.COOLDOWN_AFTER_SPEECH:
            return False

        self.last_spoken_time = now
        self.last_spoken_name = name
        full_announcement = f"{config.GREETING_TEMPLATE.format(name=name)} {config.UNLOCK_MESSAGE}"
        self.speak(full_announcement, play_chime=True, force=True)
        return True

    def speak_registration_success(self, name: str):
        """Speaks welcome announcement upon completing face registration."""
        msg = config.REGISTRATION_MESSAGE.format(name=name)
        self.last_spoken_time = time.time()
        self.last_spoken_name = name
        self.speak(msg, play_chime=True, force=True)

    def speak_greeting(self, name: str) -> bool:
        """Compatibility wrapper for speak_welcome."""
        return self.speak_welcome(name)

    def reset_cooldown(self):
        """Resets the cooldown timer."""
        self.last_spoken_time = 0.0
        self.last_spoken_name = None

# Singleton instance accessor
voice = VoiceEngine()
