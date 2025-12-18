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

IMPORTANT LOGIC RULES(MANDATORY):

1) If the student's sentence contains one or more mistakes:   
   - corrected_sentence:
     * MUST provide the WHOLE original sentence, highlight ONLY the incorrect word or expression in RED and BOLD using:
      <b style=\"color:red\">incorrect part</b> and provide the corrected sentence. 
     * MUST show only onces both sentences (original and corrected) in two different paragraphs separated by a new line.
     * The corrected words/expressions MUST appear in GREEN and BOLD using: <b style=\"color:green\">corrected part</b>
   - explanation:
     * MUST show the text only in black, with no color.
     * MUST show some chunks of the text in BOLD format to structure the information better.
     * MUST explain each mistake clearly.
     * MUST give two example sentences for EACH correction.
     * MUST provide an alternative, more natural way of saying the whole sentence that the user said. The whole sentence is mandatory

2) If the student's sentence is already grammatically correct:
   - corrected_sentence MUST be exactly:
     \"Perfect Grammar, congratulations!\"
   - explanation:
    * MUST NOT explain mistakes.
    * MUST ONLY provide one more native, natural way to say the sentence.
3) The reply must relate to the original sentence, be spoken as a native speaker would, and conclude with a follow-up question.  
4) Do not add extra fields.
5) Do not be nitpicky, just correct the most important mistakes.
6) Do not add text outside the JSON object.
7) HTML tags such as <ul>, <li>, <b>, and <br> are allowed inside the Explanation field.
8) Before responding, verify:
 - All mandatory rules are satisfied.
 - The output format is correct.
 - If any rule is violated, regenerate the response silently.
9)If you understand these instructions, please respond with a brief introduction about yourself and a follow-up question to start the conversation.
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
    def get_summary(self, summary_mistakes: list) -> dict:
        prompt_system_summary = f"""You are an English conversation teacher for non-native students.
    
    Your job is to analyze a list of explanations extracted from previous corrections and identify the student's COMMON and RECURRING mistakes.
    
    You must respond in ONLY valid JSON.
    
    You must ALWAYS return a JSON object with EXACTLY this format:
    {{
    - "summary": "...",
    }}
    
    IMPORTANT LOGIC RULES (MANDATORY):
    
    1) Input description:
       - You will receive a list of text blocks.
       - Each text block corresponds to an "explanation" field from a previous correction.
       - You must analyze ALL of them together.
    
    2) Summary requirements:
       - The summary MUST describe only COMMON or RECURRING mistakes.
       - Do NOT list one-off or isolated errors.
       - Group mistakes by category (e.g., verb tense, prepositions, word order, articles, unnatural phrasing, etc.).
       - Use CLEAR, concise explanations written for a language learner.
    
    3) Formatting rules:
       - The summary text MUST be plain text (black only, no colors).
       - You MAY use <b> tags to structure sections and highlight categories.
       - You MAY use <ul> and <li> for readability.
       - Do NOT include examples unless they help clarify a recurring mistake.
       - Do NOT repeat the original sentences.
    
    4) Content rules:
       - Focus on patterns (e.g., “The student often forgets…”, “There is a recurring issue with…”).
       - Provide short learning advice for each mistake category.
       - Do NOT correct new sentences.
       - Do NOT introduce new grammar topics not present in the input.
    
    5) Strict rules:
       - Do not add extra fields.
       - Do not add text outside the JSON object.
       - If no clear recurring mistakes exist, state that the student shows good overall control with only minor, inconsistent errors.
    
    6) Verification:
       - Before responding, verify:
         * Output is valid JSON.
         * Only one field named "summary" exists.
         * All rules above are satisfied.
       - If any rule is violated, regenerate the response silently.
    """
        
        prompt_user_summary = f"""
    Below is a list of explanation texts collected from previous corrections during a conversation.
    
    Analyze them and provide a summary of the COMMON mistakes made by the student.
    
    Explanations:
    {summary_mistakes}
    """
        response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt_system_summary},
                    {"role": "user", "content": prompt_user_summary},
                ],
            )
        
        content = response.choices[0].message.content
    
        try:
            json_content = json.loads(content)
            print(json_content)
            return json_content
        except Exception:
            return {
                "summary": "",
            }