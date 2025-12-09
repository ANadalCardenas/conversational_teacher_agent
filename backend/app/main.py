from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .chatgpt_client import ChatGPTClient

from .speech_to_text import SpeechToText

# --- FastAPI app ---
app = FastAPI(title="Conversational Teacher Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- OpenAI client --- 
# Automatically reads OPENAI_API_KEY from environment
client = ChatGPTClient()

# --- Models ---
class SummaryRequest(BaseModel):
    dummy: bool | None = None


class SummaryResponse(BaseModel):
    main_mistakes: list[str]
    activities: list[str]


# --- Global STT instance (model loaded once at startup) ---
stt = SpeechToText(model_name="base", language="en")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/voice-turn")
async def voice_turn(audio: UploadFile = File(...)):
    """
    Receives audio from the frontend and:
      1) Runs Whisper speech-to-text to get the transcription
      2) Calls the conversational teacher agent to get:
         - corrected sentence
         - explanation of corrections
         - follow-up reply

    Frontend expects:
      - original_sentence
      - corrected_sentence
      - explanation
      - reply
    """

    # Read raw bytes
    content = await audio.read()
    # Determine extension (fall back to 'webm' like the frontend)
    ext = "webm"
    if audio.filename and "." in audio.filename:
        ext = audio.filename.rsplit(".", 1)[-1].lower()

    # Transcribe audio
    text = stt.transcribe_bytes(content, file_extension=ext)

    analysis = client.analyze_sentence(text)

    # Safety guard: if something went wrong and analysis is not a dict
    if not isinstance(analysis, dict):
        analysis = {
            "corrected_sentence": "",
            "explanation": "Unexpected response format from language model.",
            "reply": str(analysis),
        }

    original_sentence = text
    corrected_sentence = analysis.get("corrected_sentence", "")
    explanation = analysis.get("explanation", "")
    reply = analysis.get("reply", "")

    # 5) Return everything to the frontend
    return {
        "original_sentence": original_sentence,
        "corrected_sentence": corrected_sentence,
        "explanation": explanation,
        "reply": reply,
    }



@app.post("/api/summary", response_model=SummaryResponse)
async def summary(_: SummaryRequest):
    """
    Returns a summary of the session:
      - main mistakes
      - proposed activities for improvement
    """
    # TODO: Call your summary agent here!
    ####################################################
    ####################################################
    summary = client.get_summary(full_conversation)

    mistakes = summary.get("summary_mistakes", [])
    activities = summary.get("summary_activities", "")

    return SummaryResponse(
        main_mistakes=mistakes,
        activities=activities
    )
