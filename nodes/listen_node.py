import speech_recognition as sr
import logging
from typing import Optional

class ListenNode:
    """
    Speech-to-Text node (mic to text).
    Optional: microphone selection.
    """

    def __init__(
        self,
        language: str = "en",
        mic_index: Optional[int] = None
    ):
        self.language = language
        self.mic_index = mic_index
        self.recognizer = sr.Recognizer()

    @staticmethod
    def list_microphones():
        print("\n--- Available Microphones ---")
        for idx, name in enumerate(sr.Microphone.list_microphone_names()):
            print(f"#{idx}: {name}")
        print("-----------------------------\n")

    def run(self) -> Optional[str]:
        if self.mic_index is not None:
            mic = sr.Microphone(device_index=self.mic_index)
        else:
            mic = sr.Microphone()

        with mic as source:
            print("🔊 Listening... (waiting for ambient noise adjustment)")
            logging.info("🔊 Listening... (ambient noise adjustment)")
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            print(f"[ListenNode] Threshold: {self.recognizer.energy_threshold}")

            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("[ListenNode] Timeout before speech detected.")
                logging.warning("[ListenNode] Timeout before speech detected.")
                return None

        try:
            lang_code = "en-US"
            text = self.recognizer.recognize_google(audio, language=lang_code)
            print(f"🗣️ User: {text}")
            logging.info(f"🗣️ User: {text}")
            return text
        except sr.UnknownValueError:
            print("[ListenNode] Could not understand audio.")
            logging.warning("[ListenNode] Could not understand audio.")
            return None
        except sr.RequestError as e:
            print(f"[ListenNode] API error: {e}")
            logging.error(f"[ListenNode] API error: {e}")
            return None

def listen_node(state):
    node = ListenNode(language=state.get("language", "en"))
    text = node.run()
    state["user_input"] = text
    return state
