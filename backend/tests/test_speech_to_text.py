import os
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from app.speech_to_text import SpeechToText, WHISPER_SR


@pytest.fixture
def stt():
    """Return a SpeechToText instance with the Whisper model already mocked."""
    instance = SpeechToText(model_name="base", language="en")
    return instance


# ---------------------------------------------------------------------------
# __init__
# ---------------------------------------------------------------------------


class TestInit:
    def test_model_is_loaded_with_correct_name(self):
        with patch("whisper.load_model", return_value=MagicMock()) as mock_load:
            SpeechToText(model_name="small", language="en")
            mock_load.assert_called_once_with("small", device=mock_load.call_args.kwargs["device"])

    def test_language_is_stored(self, stt):
        assert stt.language == "en"

    def test_device_is_cpu_or_cuda(self, stt):
        assert stt.device in ("cpu", "cuda")


# ---------------------------------------------------------------------------
# transcribe_bytes — normal audio
# ---------------------------------------------------------------------------


class TestTranscribeBytes:
    def test_returns_transcribed_text_for_normal_audio(self, stt):
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.1  # above threshold

        with patch("whisper.load_audio", return_value=audio_array):
            stt.model.transcribe.return_value = {"text": " Hello world "}
            result = stt.transcribe_bytes(b"fake audio bytes", file_extension="wav")

        assert result == "Hello world"

    def test_returns_empty_string_for_silent_audio(self, stt):
        silent_audio = np.zeros(WHISPER_SR, dtype=np.float32)  # mean amplitude == 0

        with patch("whisper.load_audio", return_value=silent_audio):
            result = stt.transcribe_bytes(b"silent audio bytes", file_extension="wav")

        stt.model.transcribe.assert_not_called()
        assert result == ""

    def test_strips_whitespace_from_transcription(self, stt):
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.2

        with patch("whisper.load_audio", return_value=audio_array):
            stt.model.transcribe.return_value = {"text": "   trimmed   "}
            result = stt.transcribe_bytes(b"audio", file_extension="webm")

        assert result == "trimmed"

    def test_returns_empty_string_when_transcribe_text_is_none(self, stt):
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.1

        with patch("whisper.load_audio", return_value=audio_array):
            stt.model.transcribe.return_value = {"text": None}
            result = stt.transcribe_bytes(b"audio", file_extension="wav")

        assert result == ""

    def test_default_extension_is_webm(self, stt):
        """transcribe_bytes should accept a call without specifying file_extension."""
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.1

        with patch("whisper.load_audio", return_value=audio_array):
            stt.model.transcribe.return_value = {"text": "ok"}
            result = stt.transcribe_bytes(b"audio")

        assert result == "ok"

    def test_temp_file_is_removed_after_transcription(self, stt):
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.1
        created_paths = []

        original_load_audio = __import__("whisper").load_audio

        def capture_path(path):
            created_paths.append(path)
            return audio_array

        with patch("whisper.load_audio", side_effect=capture_path):
            stt.model.transcribe.return_value = {"text": "hello"}
            stt.transcribe_bytes(b"audio", file_extension="wav")

        assert len(created_paths) == 1
        assert not os.path.exists(created_paths[0]), "Temp file should be deleted after transcription"

    def test_temp_file_is_removed_even_on_transcription_error(self, stt):
        audio_array = np.ones(WHISPER_SR, dtype=np.float32) * 0.1
        created_paths = []

        def capture_path(path):
            created_paths.append(path)
            return audio_array

        with patch("whisper.load_audio", side_effect=capture_path):
            stt.model.transcribe.side_effect = RuntimeError("GPU error")
            with pytest.raises(RuntimeError):
                stt.transcribe_bytes(b"audio", file_extension="wav")

        assert len(created_paths) == 1
        assert not os.path.exists(created_paths[0]), "Temp file should be deleted even when an error occurs"

    def test_whisper_silence_threshold_boundary(self, stt):
        """Audio exactly at the threshold should be treated as silent."""
        threshold = 0.005
        audio_at_threshold = np.full(WHISPER_SR, threshold, dtype=np.float32)

        with patch("whisper.load_audio", return_value=audio_at_threshold):
            result = stt.transcribe_bytes(b"audio", file_extension="wav", silence_threshold=threshold)

        assert result == ""
