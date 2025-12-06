from openai import OpenAI
import json

class ChatGPTClient:
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = OpenAI()
        self.model = model

    def analyze_sentence(self, sentence: str) -> dict:
        prompt = f"""
You are an English teacher. Your task is to analyze a student's sentence and respond ONLY with a JSON object.

STUDENT SENTENCE:
"{sentence}"

REQUIRED JSON FORMAT (use exactly these keys):

{{
  "corrected_sentence": "...",
  "explanation": "...",
  "examples": ["...", "...", "..."],
  "reply": "..."
}}

RULES:
- Your entire response MUST be valid JSON.
- Do NOT include any text outside the JSON.
- Do NOT add comments or explanations outside the JSON.
- If the sentence has no mistakes, correct it only lightly and still fill the fields.

"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a strict language-teaching assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except Exception:
            return {
                "corrected_sentence": "",
                "explanation": "Parsing error.",
                "examples": [],
                "reply": content,
            }
"""
if __name__ == "__main__":
    # Simple manual test
    text = "Hello, whats se result to add 1 and 2?"
    reply = ask_chatgpt(text)
    print("Assistant:", reply)
    """