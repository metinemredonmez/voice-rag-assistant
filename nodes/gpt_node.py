import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class GPTNode:
    """
    OpenAI GPT-based response generator node.
    Stores message history and supports context-aware responses.
    """

    def __init__(self, language: str = "en"):
        self.language = language
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.message_history = []

    def run(self, user_input: str, context: str = "", reset_history: bool = False) -> str:
        """
        Generates a response from the GPT model based on user input (and optional context).
        Optionally resets message history to avoid carrying old context.

        Args:
            user_input (str): Text from the user.
            context (str): Additional info from Wikipedia or other sources (optional).
            reset_history (bool): If True, clears past conversation history.

        Returns:
            str: GPT response.
        """
        system_prompt = "Speak English and stick to the context."

        if reset_history or not self.message_history:
            self.message_history = [{"role": "system", "content": system_prompt}]

        if context:
            user_msg = f"Question: {user_input}\nContext: {context}"
        else:
            user_msg = user_input

        self.message_history.append({"role": "user", "content": user_msg})

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.message_history,
            )
            reply = response.choices[0].message.content.strip()
            logging.info(f"[GPTNode] Response: {reply}")
            self.message_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            logging.error(f"[GPTNode] API error: {e}")
            return "GPT response could not be retrieved."

    def reset_memory(self) -> None:
        """Resets message history to clear previous context."""
        self.message_history = []

def gpt_node(state):
    node = GPTNode(language=state.get("language", "en"))
    reset = state.get("reset_history", False)
    answer = node.run(state.get("user_input", ""), context=state.get("context", ""), reset_history=reset)
    state["answer"] = answer
    # Reset flag after use
    state["reset_history"] = False
    return state
