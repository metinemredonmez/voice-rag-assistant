import pyttsx3
import time
from gtts import gTTS
from playsound import playsound
import os
import logging

class SpeakNode:
    """
    Text-to-Speech node supporting pyttsx3 and gTTS.
    """

    def __init__(self, tts_method: str = "pyttsx3", language: str = "tr"):
        self.tts_method = tts_method.lower()
        self.language = language

    def run(self, text: str, language: str = None) -> None:
        if not text:
            logging.warning("[SpeakNode] Received empty text.")
            return

        lang = language if language else self.language

        if self.tts_method == "pyttsx3":
            self._speak_pyttsx3(text, lang)
        elif self.tts_method == "gtts":
            self._speak_gtts(text, lang)
        else:
            logging.error(f"[SpeakNode] Unknown TTS method: {self.tts_method}")

    def _speak_pyttsx3(self, text: str, language: str) -> None:
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 1.0)

            voices = engine.getProperty('voices')
            selected_voice = None

            if language == "tr":
                # Türkçe için özellikle "Yelda" sesini bul!
                for voice in voices:
                    if "yelda" in voice.name.lower():
                        selected_voice = voice.id
                        break
                if not selected_voice:
                    # Alternatif olarak 'tr_' ile başlayan veya Türkçe olan ilk voice’u seç
                    for voice in voices:
                        if "tr_" in voice.id.lower() or "turkish" in voice.name.lower():
                            selected_voice = voice.id
                            break
                if not selected_voice:
                    selected_voice = voices[0].id  # fallback

            elif language == "en":
                # İngilizce için kaliteli kadın seslerinden birini seç (ör: Samantha, Anna, Amelie)
                for pref in ["samantha", "anna", "amelie", "alice"]:
                    for voice in voices:
                        if pref in voice.name.lower():
                            selected_voice = voice.id
                            break
                    if selected_voice:
                        break
                if not selected_voice:
                    selected_voice = voices[0].id  # fallback

            else:
                selected_voice = voices[0].id

            engine.setProperty('voice', selected_voice)
            logging.info(f"[SpeakNode] Using voice: {selected_voice}")
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            logging.error(f"[SpeakNode] pyttsx3 error: {e}")

    def _speak_gtts(self, text: str, language: str) -> None:
        try:
            tts = gTTS(text=text, lang=language)
            filename = f"temp_audio_{int(time.time())}.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except Exception as e:
            logging.error(f"[SpeakNode] gTTS error: {e}")

def speak_node(state):
    reply = state.get("answer", "")
    language = state.get("language", "tr")
    node = SpeakNode(language=language)
    node.run(reply, language)
    return state
