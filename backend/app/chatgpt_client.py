from openai import OpenAI


class ChatGPTClient:
    def __init__(self, model: str = "gpt-4.1-mini"):
        """
        Initializes the OpenAI client.
        Automatically reads OPENAI_API_KEY from the environment.
        """
        self.client = OpenAI()
        self.model = model

    def ask(self, prompt: str) -> str:
        """
        Sends a message to ChatGPT and returns the assistant's reply.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )

        return response.choices[0].message.content


"""
if __name__ == "__main__":
    # Simple manual test
    text = "Hello, whats se result to add 1 and 2?"
    reply = ask_chatgpt(text)
    print("Assistant:", reply)
    """