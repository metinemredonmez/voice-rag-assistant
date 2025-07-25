"""
A2A Orchestration:
A minimal orchestrator node that fetches information from multiple "agents" (RAG) and then generates a context-aware response using GPT.

Usage:
    answer = a2a_orchestration("Who is Atatürk?", language="tr")
    print(answer)

Agents:
    - FactAgent: fetches information from Wikipedia via RAG
    - ChatAgent: generates answer to the question using GPT and the fetched information
"""

from nodes.rag_node import RAGNode
from nodes.gpt_node import GPTNode

class FactAgent:
    """
    Agent that fetches context from Wikipedia (RAG).
    """
    def __init__(self, language="en"):
        self.rag = RAGNode(language)

    def fetch_fact(self, query: str) -> str:
        """
        Retrieves summary from Wikipedia based on user question.
        """
        return self.rag.run(query)

class ChatAgent:
    """
    Agent that produces the final answer using GPT (LLM).
    """
    def __init__(self, language="en"):
        self.gpt = GPTNode(language)

    def chat(self, question: str, fact: str) -> str:
        """
        Generates an answer using the question and retrieved fact/context.
        """
        return self.gpt.run(question, context=fact)

def a2a_orchestration(user_question: str, language: str = "en") -> str:
    """
    Returns the final answer through the chain: Question → FactAgent → ChatAgent.

    Args:
        user_question (str): Natural language question from the user
        language (str): "tr" or "en"

    Returns:
        str: GPT's response (supported by fact)
    """
    fact_agent = FactAgent(language)
    chat_agent = ChatAgent(language)
    fact = fact_agent.fetch_fact(user_question)
    return chat_agent.chat(user_question, fact)

# -- EXAMPLE USAGE --
if __name__ == "__main__":
    result = a2a_orchestration("What is the largest island in the world?", language="tr")
    print(result)
