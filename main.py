from nodes.command_node import CommandNode
from nodes.gpt_node import GPTNode
from nodes.listen_node import ListenNode
from nodes.rag_node import RAGNode
from nodes.speak_node import SpeakNode


def is_greeting(text):
    GREETINGS = {"hello", "hi", "hey", "good morning", "good evening", "goodbye", "bye", "thanks", "thank you"}
    return text and text.lower().strip() in GREETINGS

def main():
    lang = "en"
    listen_node = ListenNode(language=lang)
    speak_node = SpeakNode(language=lang)
    rag_node = RAGNode(language=lang)
    gpt_node = GPTNode(language=lang)
    command_node = CommandNode(language=lang)
    memory = []

    speak_node.run("Hello! I am your voice assistant.", lang)
    fail_count = 0

    while True:
        user_text = listen_node.run()
        if not user_text:
            fail_count += 1
            print(f"Could not understand input. Attempt {fail_count}/3.")
            if fail_count >= 3:
                print("Could not understand 3 times. Program is terminating.")
                break
            continue
        fail_count = 0

        cmd, lang = command_node.run(user_text)
        if cmd == "__exit__":
            break
        elif cmd == "__reset__":
            memory = []
            gpt_node.message_history = []
            continue
        elif cmd in ["__continue__", None]:
            continue
        else:
            listen_node.language = "en"
            speak_node.language = "en"
            rag_node.language = "en"
            gpt_node.language = "en"


            if is_greeting(cmd) or len(cmd.strip().split()) < 2:
                context = ""
            else:
                context = rag_node.run(cmd)

            print(f"[DEBUG] GPT prompt: {cmd} | context: {context[:100]}")
            reply = gpt_node.run(cmd, context=context)
            speak_node.run(reply, "en")

if __name__ == "__main__":
    main()
