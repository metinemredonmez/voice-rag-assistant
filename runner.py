from orchestration.voice_graph import build_voice_graph
import logging

def main() -> None:
    """
    Starts the Voice Assistant system (for LangGraph demo/testing).
    """
    logging.basicConfig(filename="logs/assistant.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    print("🔁 Starting Voice Assistant (LangGraph mode)...")
    graph = build_voice_graph()
    graph.invoke({})

if __name__ == "__main__":
    main()
