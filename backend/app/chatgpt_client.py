from openai import OpenAI
import json


class ChatGPTClient:
    def __init__(self, model: str = "gpt-4.1"):
        self.client = OpenAI()
        self.model = model

    def analyze_sentence(self, sentence: str) -> dict:
        prompt_system = f"""You are an English conversation teacher for non-native students.
Your job is to analyze the student's sentence and respond in ONLY valid JSON.

You must ALWAYS return a JSON object with EXACTLY format:
{{
- "corrected_sentence": "...",
- "explanation": "...",
- "reply": "...",
}}

IMPORTANT LOGIC RULES:

1) If the student's sentence contains one or more mistakes:   
   - corrected_sentence:
     * MUST provide the original sentence, highlight ONLY the incorrect word or expression in RED and BOLD using:
      <b style=\"color:red\">incorrect part</b> and provide the corrected sentence. 
     * MUST show only onces both sentences (original and corrected).
     * The corrected words/expressions MUST appear in GREEN and BOLD using: <b style=\"color:green\">corrected part</b>
   - explanation:
     * MUST show the text only in black, with no color.
     * MUST show some chunks of the text in BOLD format to structure the information better.
     * MUST explain each mistake clearly.
     * MUST give two example sentences for EACH correction.
     * MUST provide an alternative, more natural way of saying the whole sentence that the user said.

2) If the student's sentence is already grammatically correct:
   - corrected_sentence MUST be exactly:
     \"Perfect Grammar, congratulations!\"
   - explanation:
    * MUST NOT explain mistakes.
    * MUST ONLY provide one more native, natural way to say the sentence.
3) The reply must relate to the original sentence, be spoken as a native speaker would, and conclude with a follow-up question.  
Do not add extra fields.
Do not be nitpicky, just correct the most important mistakes.
Do not add text outside the JSON object.
HTML tags such as <ul>, <li>, <b>, and <br> are allowed inside the Explanation field.
"""
        prompt_user = f"""
A student says the following sentence:

\"{sentence}\"

Analyze the sentence and respond following ALL the rules given in the system prompt.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt_system},
                {"role": "user", "content": prompt_user},
            ],
        )

        content = response.choices[0].message.content

        try:
            json_content = json.loads(content)
            print(json_content)
            return json_content
        except Exception:
            return {
                "corrected_sentence": "",
                "explanation": "Parsing error.",
                "reply": content,
            }

