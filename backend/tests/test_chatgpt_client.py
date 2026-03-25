import json
from unittest.mock import MagicMock

import pytest

from app.chatgpt_client import ChatGPTClient


@pytest.fixture
def mock_response():
    """Factory that builds a fake OpenAI chat completion response."""

    def _make(content: str):
        message = MagicMock()
        message.content = content
        choice = MagicMock()
        choice.message = message
        response = MagicMock()
        response.choices = [choice]
        return response

    return _make


@pytest.fixture
def chatgpt_client():
    return ChatGPTClient(model="gpt-test")


# ---------------------------------------------------------------------------
# analyze_sentence
# ---------------------------------------------------------------------------


class TestAnalyzeSentence:
    def test_valid_json_response_is_returned_as_dict(self, chatgpt_client, mock_response):
        expected = {
            "original_sentence": 'I <b style="color:red">goes</b> to school',
            "corrected_sentence": 'I <b style="color:green">go</b> to school',
            "explanation": "Use 'go' for first-person singular.",
            "reply": "Good effort! Do you go to school every day?",
            "error_prompt": "",
        }
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            json.dumps(expected)
        )

        result = chatgpt_client.analyze_sentence("I goes to school")

        assert result == expected

    def test_invalid_json_returns_fallback_dict(self, chatgpt_client, mock_response):
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            "not valid json {"
        )

        result = chatgpt_client.analyze_sentence("some sentence")

        assert result["original_sentence"] == ""
        assert result["corrected_sentence"] == ""
        assert result["explanation"] == "Parsing error."
        assert result["reply"] == "not valid json {"
        assert result["error_prompt"] == ""

    def test_sentence_is_included_in_user_prompt(self, chatgpt_client, mock_response):
        valid_payload = json.dumps(
            {
                "original_sentence": "test",
                "corrected_sentence": "test",
                "explanation": "",
                "reply": "Nice!",
                "error_prompt": "",
            }
        )
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            valid_payload
        )

        chatgpt_client.analyze_sentence("Hello world")

        call_kwargs = chatgpt_client.client.chat.completions.create.call_args.kwargs
        messages = call_kwargs["messages"]
        user_message = next(m for m in messages if m["role"] == "user")
        assert "Hello world" in user_message["content"]

    def test_configured_model_is_used(self, chatgpt_client, mock_response):
        valid_payload = json.dumps(
            {
                "original_sentence": "",
                "corrected_sentence": "",
                "explanation": "",
                "reply": "",
                "error_prompt": "",
            }
        )
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            valid_payload
        )

        chatgpt_client.analyze_sentence("test")

        call_kwargs = chatgpt_client.client.chat.completions.create.call_args.kwargs
        assert call_kwargs["model"] == "gpt-test"

    def test_perfect_grammar_response_is_parsed(self, chatgpt_client, mock_response):
        expected = {
            "original_sentence": "I go to school every day.",
            "corrected_sentence": "Perfect Grammar, congratulations!",
            "explanation": "A more natural way: 'I attend school daily.'",
            "reply": "Excellent! What subjects do you enjoy?",
            "error_prompt": "",
        }
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            json.dumps(expected)
        )

        result = chatgpt_client.analyze_sentence("I go to school every day.")

        assert result["corrected_sentence"] == "Perfect Grammar, congratulations!"


# ---------------------------------------------------------------------------
# get_summary
# ---------------------------------------------------------------------------


class TestGetSummary:
    def test_valid_json_response_is_returned_as_dict(self, chatgpt_client, mock_response):
        expected = {
            "summary_mistakes": "Recurring issues with verb tense.",
            "activities": "I __ to school. Options(go, goes, went).\nSolution: go.",
        }
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            json.dumps(expected)
        )

        result = chatgpt_client.get_summary(["explanation one", "explanation two"])

        assert result == expected

    def test_invalid_json_returns_minimal_dict(self, chatgpt_client, mock_response):
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            "not json at all"
        )

        result = chatgpt_client.get_summary(["explanation one"])

        assert isinstance(result, dict)
        assert "summary" in result

    def test_mistakes_list_is_included_in_user_prompt(self, chatgpt_client, mock_response):
        valid_payload = json.dumps({"summary_mistakes": "ok", "activities": "ok"})
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            valid_payload
        )
        mistakes = ["mistake alpha", "mistake beta"]

        chatgpt_client.get_summary(mistakes)

        call_kwargs = chatgpt_client.client.chat.completions.create.call_args.kwargs
        messages = call_kwargs["messages"]
        user_message = next(m for m in messages if m["role"] == "user")
        assert "mistake alpha" in user_message["content"]

    def test_empty_mistakes_list_returns_valid_response(self, chatgpt_client, mock_response):
        valid_payload = json.dumps(
            {
                "summary_mistakes": "No recurring mistakes detected.",
                "activities": "General mixed review activity.",
            }
        )
        chatgpt_client.client.chat.completions.create.return_value = mock_response(
            valid_payload
        )

        result = chatgpt_client.get_summary([])

        assert "summary_mistakes" in result
        assert "activities" in result
