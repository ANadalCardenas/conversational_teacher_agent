import sys
from unittest.mock import MagicMock, patch

# Mock heavy dependencies if not installed (e.g. in CI environments).
# When installed (e.g. in Docker), the real packages are used as-is.
try:
    import whisper  # noqa: F401
except ImportError:
    sys.modules["whisper"] = MagicMock()

try:
    import torch  # noqa: F401
except ImportError:
    sys.modules["torch"] = MagicMock()

# Patch external dependencies before any app modules are imported.
# This prevents actual model loading and OpenAI client initialization during tests.
patch("whisper.load_model", return_value=MagicMock()).start()
patch("openai.OpenAI", return_value=MagicMock()).start()
