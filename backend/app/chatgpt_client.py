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
You must also generate practice activities to help the student avoid these mistakes in the future.

You must respond in ONLY valid JSON.

You must ALWAYS return a JSON object with EXACTLY this format:
{{
  "summary_mistakes": "...",
  "activities": "..."
}}

IMPORTANT LOGIC RULES (MANDATORY):

For the "summary_mistakes" field:
    
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
       - Do NOT repeat the original sentences.
    
    4) Content rules:
       - Focus on patterns (e.g., “The student often forgets…”, “There is a recurring issue with…”).
       - Provide short learning advice for each mistake category.
       - Do NOT correct new sentences.
       - Do NOT introduce new grammar topics not present in the input.

For the "activities" field:

    1) Purpose:
       - Activities must help the student PRACTISE and AVOID their COMMON mistakes.
       - Each activity MUST be directly related to one of the recurring mistake categories identified in "summary_mistakes".
    
    2) Quantity:
       - Generate EXACTLY THREE (3) activities for EACH recurring mistake category.
    
    3) Activity format (MANDATORY):
       Each activity must follow this exact structure:

       Sentence with a blank. Options(option1, option2, option3).
       Solution: Correct full sentence.
       Explanation: Short explanation of the grammar rule.

       Example:
       I like _______ hiking every day. Options(go, to go, went).
       Solution: I like to go hiking every day.
       Explanation: After "like", we usually use "to + verb".

    4) Formatting rules:
       - The activities field MUST be a single plain-text string.
       - You MAY separate activities using line breaks or bullet points.
       - Do NOT use JSON arrays or objects inside the string.
       - Do NOT include emojis or special formatting.
    
    5) Content rules:
       - Use simple, clear language suitable for an English learner.
       - Do NOT reuse the same sentence structure repeatedly.
       - Do NOT introduce grammar topics not found in the summary.
       - Ensure only ONE correct option per activity.

Global strict rules:
    - Do not add extra fields.
    - Do not add text outside the JSON object.
    - If no clear recurring mistakes exist:
        * "summary_mistakes" should state that the student shows good overall control with only minor, inconsistent errors.
        * "activities" should include general mixed review activities based on the minor patterns observed.

Verification (MANDATORY before responding):
    - Output is valid JSON.
    - EXACTLY two fields exist: "summary_mistakes" and "activities".
    - Both fields are strings.
    - All rules above are satisfied.
    - If any rule is violated, regenerate the response silently.
"""
        
        prompt_user_summary = f"""
Below is a list of explanation texts collected from previous corrections during a conversation.

Analyze them and provide:
1) A summary of the COMMON recurring mistakes.
2) Practice activities to help the student avoid those mistakes.

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