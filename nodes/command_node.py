from nodes.speak_node import SpeakNode

class CommandNode:
    """
    Handles commands such as exit, reset, help, etc.
    """

    def __init__(self, language: str = "en"):
        self.language = language
        self.speaker = SpeakNode(language=language)

    def run(self, text: str):
        if not text:
            return None, self.language

        lowered = text.lower().strip()

        if lowered in ["quit", "exit"]:
            self.speaker.run("Goodbye!", self.language)
            return "__exit__", self.language

        elif lowered in ["help", "commands"]:
            help_text = {
                "en": "Commands: help, quit, reset."
            }
            self.speaker.run(help_text.get(self.language, help_text["en"]), self.language)
            return "__continue__", self.language

        elif lowered in ["reset"]:
            self.speaker.run("Conversation history cleared.", self.language)
            return "__reset__", self.language

        return text, self.language

def command_node(state):
    node = CommandNode(language=state.get("language", "en"))
    result, language = node.run(state.get("user_input", ""))
    state["language"] = language
    state["user_input"] = result

    if result == "__reset__":
        state["reset_history"] = True
    else:
        state["reset_history"] = False

    return state
