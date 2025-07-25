from orchestration.voice_graph import build_voice_graph
import logging

def main() -> None:
    """
    Starts the Voice Assistant system (LangGraph-based).
    """
    logging.basicConfig(filename="logs/assistant.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    print("🎙️ Starting Voice Assistant (LangGraph-based)...")
    graph = build_voice_graph()
    graph.invoke({})

if __name__ == "__main__":
    main()
