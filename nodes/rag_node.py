import wikipedia
import logging

print("[DEBUG] Wikipedia module default language:", wikipedia.languages()["en"])
wikipedia.set_lang("en")

class RAGNode:
    """
    Wikipedia-based Retrieval-Augmented Generation (RAG) node.
    Retrieves a short context from Wikipedia based on the user's question.
    """

    def __init__(self, language: str = "en"):
        self.language = "en"
        self.set_lang()

    def set_lang(self, language: str = "en") -> None:
        wikipedia.set_lang("en")
        self.language = "en"
        print("[DEBUG] Wikipedia language set to:", wikipedia.languages()["en"])

    def run(self, query: str) -> str:
        print("[DEBUG] Wikipedia language IN RUN:", wikipedia.languages()["en"])
        try:
            logging.info(f"[RAGNode] Searching Wikipedia for: {query}")
            results = wikipedia.search(query)
            if not results:
                logging.warning("[RAGNode] No results found.")
                return ""

            try:
                page = wikipedia.page(results[0], auto_suggest=False)
            except wikipedia.DisambiguationError as e:
                logging.warning(f"[RAGNode] Disambiguation found: {e.options}")
                page = wikipedia.page(e.options[0])
            except wikipedia.PageError:
                logging.warning("[RAGNode] Page not found.")
                return ""

            content = page.content[:1000]
            logging.info("[RAGNode] Wikipedia content retrieved successfully.")
            return content

        except Exception as e:
            logging.error(f"[RAGNode] Wikipedia error: {e}")
            return ""

def rag_node(state):
    node = RAGNode(language="en")
    context = node.run(state.get("user_input", ""))
    state["context"] = context
    return state
