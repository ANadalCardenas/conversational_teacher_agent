from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_summary_mistakes():
    """Clear the global summary list before and after every test."""
    main_module.summary_mistakes.clear()
    yield
    main_module.summary_mistakes.clear()


# ---------------------------------------------------------------------------
# GET /health
# ---------------------------------------------------------------------------


class TestHealth:
    def test_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_returns_ok_status(self, client):
        response = client.get("/health")
        assert response.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# POST /api/voice-turn
# ---------------------------------------------------------------------------


SAMPLE_ANALYSIS = {
    "original_sentence": 'I <b style="color:red">goes</b> to school',
    "corrected_sentence": 'I <b style="color:green">go</b> to school',
    "explanation": "Use 'go' for first-person singular present tense.",
    "reply": "Good effort! Do you enjoy school?",
    "error_prompt": "",
}


class TestVoiceTurn:
    def test_returns_200_with_valid_audio(self, client):
        main_module.stt.transcribe_bytes = MagicMock(return_value="I goes to school")
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        response = client.post(
            "/api/voice-turn",
            files={"audio": ("recording.webm", b"fake audio data", "audio/webm")},
        )

        assert response.status_code == 200

    def test_response_contains_required_fields(self, client):
        main_module.stt.transcribe_bytes = MagicMock(return_value="I goes to school")
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        response = client.post(
            "/api/voice-turn",
            files={"audio": ("recording.webm", b"fake audio data", "audio/webm")},
        )

        data = response.json()
        assert "original_sentence" in data
        assert "corrected_sentence" in data
        assert "explanation" in data
        assert "reply" in data

    def test_explanation_is_appended_to_summary_mistakes(self, client):
        main_module.stt.transcribe_bytes = MagicMock(return_value="I goes to school")
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        client.post(
            "/api/voice-turn",
            files={"audio": ("recording.webm", b"fake audio data", "audio/webm")},
        )

        assert len(main_module.summary_mistakes) == 1
        assert main_module.summary_mistakes[0] == SAMPLE_ANALYSIS["explanation"]

    def test_multiple_turns_accumulate_in_summary_mistakes(self, client):
        main_module.stt.transcribe_bytes = MagicMock(return_value="test")
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        client.post(
            "/api/voice-turn",
            files={"audio": ("r.webm", b"audio", "audio/webm")},
        )
        client.post(
            "/api/voice-turn",
            files={"audio": ("r.webm", b"audio", "audio/webm")},
        )

        assert len(main_module.summary_mistakes) == 2

    def test_file_extension_is_inferred_from_filename(self, client):
        transcribe_mock = MagicMock(return_value="hello")
        main_module.stt.transcribe_bytes = transcribe_mock
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        client.post(
            "/api/voice-turn",
            files={"audio": ("recording.ogg", b"audio data", "audio/ogg")},
        )

        call_kwargs = transcribe_mock.call_args.kwargs
        assert call_kwargs.get("file_extension") == "ogg"

    def test_defaults_to_webm_when_filename_has_no_extension(self, client):
        transcribe_mock = MagicMock(return_value="hello")
        main_module.stt.transcribe_bytes = transcribe_mock
        main_module.client.analyze_sentence = MagicMock(return_value=SAMPLE_ANALYSIS)

        client.post(
            "/api/voice-turn",
            files={"audio": ("recording", b"audio data", "audio/webm")},
        )

        call_kwargs = transcribe_mock.call_args.kwargs
        assert call_kwargs.get("file_extension") == "webm"

    def test_missing_audio_field_returns_422(self, client):
        response = client.post("/api/voice-turn", data={})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/summary
# ---------------------------------------------------------------------------


SAMPLE_SUMMARY = {
    "summary_mistakes": "Recurring verb-tense issues in first-person singular.",
    "activities": "I __ to school. Options(go, goes, went).\nSolution: go.",
}


class TestSummary:
    def test_returns_200(self, client):
        main_module.client.get_summary = MagicMock(return_value=SAMPLE_SUMMARY)

        response = client.post("/api/summary", json={})

        assert response.status_code == 200

    def test_response_contains_main_mistakes_and_activities(self, client):
        main_module.client.get_summary = MagicMock(return_value=SAMPLE_SUMMARY)

        response = client.post("/api/summary", json={})

        data = response.json()
        assert data["main_mistakes"] == SAMPLE_SUMMARY["summary_mistakes"]
        assert data["activities"] == SAMPLE_SUMMARY["activities"]

    def test_accumulated_mistakes_are_passed_to_get_summary(self, client):
        main_module.summary_mistakes.extend(["explanation A", "explanation B"])
        get_summary_mock = MagicMock(return_value=SAMPLE_SUMMARY)
        main_module.client.get_summary = get_summary_mock

        client.post("/api/summary", json={})

        get_summary_mock.assert_called_once_with(["explanation A", "explanation B"])

    def test_summary_with_empty_mistakes_list(self, client):
        main_module.client.get_summary = MagicMock(return_value=SAMPLE_SUMMARY)

        response = client.post("/api/summary", json={})

        assert response.status_code == 200
