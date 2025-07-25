import speech_recognition as sr
import logging
from typing import Optional

class TranscribeNode:
    """
    Simple Speech-to-Text node that transcribes from mic.
    """

    def __init__(self, language: str = "en"):
        self.language = language
        self.recognizer = sr.Recognizer()

    def run(self) -> Optional[str]:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            logging.info("🎤 Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            audio = self.recognizer.listen(source)

        try:
            lang_code = "tr-TR" if self.language == "tr" else "en-US"
            text = self.recognizer.recognize_google(audio, language=lang_code)
            print(f"🗣️ User: {text}")
            logging.info(f"🗣️ User: {text}")
            return text
        except sr.UnknownValueError:
            print("[TranscribeNode] Could not understand audio.")
            logging.warning("[TranscribeNode] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[TranscribeNode] API error: {e}")
            logging.error(f"[TranscribeNode] API error: {e}")
            return None

def transcribe_node(state):
    node = TranscribeNode(language=state.get("language", "tr"))
    text = node.run()
    state["user_input"] = text
    return state
