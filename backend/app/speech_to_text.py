import os
import tempfile
from typing import Optional

import numpy as np
import torch
import whisper

WHISPER_SR = 16000

class SpeechToText:
    """
    Simple wrapper around Whisper that:
    - loads the model once at startup
    - accepts raw audio bytes (e.g. from an uploaded file)
    - uses ffmpeg (via whisper.load_audio) to decode and resample to 16kHz
    """

    def __init__(self, model_name: str = "base", language: str = "en"):
        self.language = language
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"[SpeechToText] Loading Whisper model '{model_name}' on {self.device}...")
        self.model = whisper.load_model(model_name, device=self.device)
        print("[SpeechToText] Whisper model loaded.")

    def transcribe_bytes(
        self,
        audio_bytes: bytes,
        file_extension: str = "webm",
        silence_threshold: float = 0.005,
    ) -> str:
        """
        - Saves bytes to a temporary file (e.g. .webm)
        - Uses whisper.load_audio() (ffmpeg) to decode + resample
        - Runs transcription and returns the text.
        """

        # 1) Save bytes to a temporary file
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension}", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            # 2) Load + resample to 16k mono float32
            audio = whisper.load_audio(tmp_path)  # np.float32, 16000 Hz

            # 3) Simple silence check
            mean_abs = float(np.abs(audio).mean())
            print(f"[SpeechToText] Mean abs amplitude: {mean_abs:.6f}")
            if mean_abs < silence_threshold:
                print("[SpeechToText] Silence detected, skipping transcription.")
                return ""

            # 4) Transcribe with Whisper
            print("[SpeechToText] Transcribing...")
            result = self.model.transcribe(
                audio,
                fp16=(self.device == "cuda"),
                task="transcribe",
                language=self.language,
            )

            text = (result.get("text") or "").strip()
            print(f"[SpeechToText] Transcription result: {text!r}")
            return text

        finally:
            # 5) Clean up temp file
            try:
                os.remove(tmp_path)
            except OSError:
                pass
