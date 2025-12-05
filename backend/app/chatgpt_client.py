from openai import OpenAI

client = OpenAI()  # Automatically reads OPENAI_API_KEY from environment

def ask_chatgpt(prompt: str) -> str:
    """
    Sends a user message to ChatGPT and returns the assistant's response.
    """
    response = client.chat.completions.create(
        model="gpt-4.1-mini",   # or other model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )

    return response.choices[0].message.content
