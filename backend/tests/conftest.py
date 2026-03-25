from unittest.mock import MagicMock, patch

# Patch external dependencies before any app modules are imported.
# This prevents actual model loading and OpenAI client initialization during tests.
patch("whisper.load_model", return_value=MagicMock()).start()
patch("openai.OpenAI", return_value=MagicMock()).start()
