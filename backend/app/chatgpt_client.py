from openai import OpenAI
import json


class ChatGPTClient:
    def __init__(self, model: str = "gpt-4.1"):
        self.client = OpenAI()
        self.model = model

        # Store only the conversational "reply" and the raw user sentence,
        # NOT the JSON results.
        self.user_messages = []
        self.assistant_replies = []

    def _format_instruction_prompt(self):
        return """
You are an English conversational teacher.

When the user gives a sentence, RETURN STRICT JSON ONLY:

{
  "correct_sentence": "...",
  "explanation": {
        "details": "...",
        "examples": [
            "<span style='color:green; font-weight:bold'>example 1</span>",
            "<span style='color:green; font-weight:bold'>example 2</span>",
            "<span style='color:green; font-weight:bold'>example 3</span>"
        ],
        "native": "*A natural native expression related to the text*"
  },
  "reply": "..."
}

RULES:
- Highlight incorrect parts using <span style='color:red; font-weight:bold'>...</span>.
- If the sentence is already correct:
    * correct_sentence MUST equal the original sentence.
    * explanation.details MUST be "Perfect Grammar".
    * explanation.examples MUST be empty.
    * explanation.native MUST still contain a native-like expression.
- reply MUST end with a question.
- OUTPUT MUST BE VALID JSON. DO NOT add anything outside the JSON.
"""

    def analyze_sentence(self, sentence: str) -> dict:

        # Save user sentence in memory
        self.user_messages.append(sentence)

        # Build conversation context (NOT raw JSON!)
        conversation_text = ""

        for u, a in zip(self.user_messages, self.assistant_replies):
            conversation_text += f"User: {u}\nAssistant: {a}\n"

        # Add last sentence as the new user message
        conversation_text += f"User: {sentence}\n"

        messages = [
            {"role": "system", "content": "You are an English conversational teacher."},
            {"role": "system", "content": self._format_instruction_prompt()},
            {"role": "user", "content": conversation_text}
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0  # ensures stable JSON
        )

        content = response.choices[0].message.content

        # JSON decode
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError:
            return {
                "correct_sentence": "",
                "explanation": {
                    "details": "JSON parsing error",
                    "examples": [],
                    "native": ""
                },
                "reply": ""
            }

        # Save clean assistant conversational reply
        follow_up = parsed.get("reply", "")

        # Sanitize just in case
        follow_up = follow_up.replace("{", "").replace("}", "").replace('"', "'").strip()

        self.assistant_replies.append(follow_up)

        return parsed

    def get_summary(self) -> dict:

        # Build plain conversation (not JSON)
        conversation_text = ""
        for u, a in zip(self.user_messages, self.assistant_replies):
            conversation_text += f"User: {u}\nAssistant: {a}\n"

        summary_prompt = """
Analyze all user messages above. RETURN STRICT JSON:

{
  "summary_mistakes": [
     "mistake type 1",
     "mistake type 2"
  ],
  "summary_activities": "Suggestions to fix these mistakes."
}

Only list mistake TYPES, not full corrections.
"""

        messages = [
            {"role": "system", "content": "You are an English conversational teacher."},
            {"role": "system", "content": summary_prompt},
            {"role": "user", "content": conversation_text},
        ]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0
        )

        content = response.choices[0].message.content

        try:
            return json.loads(content)
        except:
            return {
                "summary_mistakes": ["JSON parsing error"],
                "summary_activities": ""
            }
