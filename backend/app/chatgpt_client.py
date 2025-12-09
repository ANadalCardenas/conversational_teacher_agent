from openai import OpenAI
import json

class ChatGPTClient:
    def __init__(self, model: str = "gpt-4.1"):
        self.client = OpenAI()
        self.model = model

    def analyze_sentence(self, sentence: str) -> dict:
        prompt = f"""
You are an English conversational teacher. Your task is to evaluate the learner’s latest sentence, correct it, provide an explanation about the mistakes and then continue the conversation with a natural follow-up response. Respond ONLY with a JSON object.
If the sentence has no mistakes, in the corrected_sentence field should appear the message 'Perfect Grammar!Congratulations!'.
If there are any mistakes in the sentence, please add next to the mistakes explanation three examples of the corrected expression or word, separated by a new line, in the explanation field.
"{sentence}"

REQUIRED JSON FORMAT (use exactly these keys):

{{
  "corrected_sentence": "...",
  "explanation": "...",
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
                "reply": content,
            }
        