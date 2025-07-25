from langgraph.graph import END, StateGraph

from nodes.transcribe_node import transcribe_node
from nodes.command_node import command_node
from nodes.rag_node import rag_node
from nodes.gpt_node import gpt_node
from nodes.speak_node import speak_node
from nodes.hallucination_checker_node import hallucination_node

import logging
import os
os.makedirs("logs", exist_ok=True)

class AssistantState(dict):
    pass

def build_voice_graph():
    graph = StateGraph(AssistantState)
    graph.add_node("transcribe", transcribe_node)
    graph.add_node("command", command_node)
    graph.add_node("rag", rag_node)
    graph.add_node("gpt", gpt_node)
    graph.add_node("hallucination", hallucination_node)
    graph.add_node("speak", speak_node)

    graph.set_entry_point("transcribe")
    graph.add_transition("transcribe", "command")
    graph.add_transition("command", "rag")
    graph.add_transition("rag", "gpt")
    graph.add_transition("gpt", "hallucination")
    graph.add_transition("hallucination", "speak")
    graph.add_transition("speak", "transcribe")
    graph.set_exit_point(END)
    return graph

def main():
    logging.basicConfig(filename="logs/assistant.log", level=logging.INFO, format="%(asctime)s - %(message)s")
    print("🎤 Starting Voice Assistant (LangGraph workflow)...")
    graph = build_voice_graph()
    graph.invoke(AssistantState())

if __name__ == "__main__":
    main()
