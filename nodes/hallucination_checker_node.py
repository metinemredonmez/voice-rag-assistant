import difflib
import openai
import os
from typing import Optional

class HallucinationChecker:
    def __init__(self, threshold: float = 0.5, emb_threshold: float = 0.80):
        self.threshold = threshold
        self.emb_threshold = emb_threshold
        self.openai_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_key:
            raise Exception("OPENAI_API_KEY environment variable is required for embeddings.")
        openai.api_key = self.openai_key

    def string_similarity(self, a: str, b: str) -> float:
        return difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def embedding_similarity(self, text1: str, text2: str) -> float:
        def get_emb(text):
            emb = openai.embeddings.create(model="text-embedding-ada-002", input=text)
            return emb.data[0].embedding

        import numpy as np
        emb1 = get_emb(text1)
        emb2 = get_emb(text2)
        v1, v2 = np.array(emb1), np.array(emb2)
        score = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return score

    def is_hallucinated(self, context: str, answer: str) -> bool:
        import re
        context_sentences = re.split(r'[.!?]\s*', context)
        context_sentences = [s for s in context_sentences if len(s.strip()) > 0]

        max_seq = max([self.string_similarity(line, answer) for line in context_sentences] or [0])
        try:
            max_emb = max([self.embedding_similarity(line, answer) for line in context_sentences] or [0])
        except Exception as e:
            print("[HallucinationChecker] Embedding error, fallback to string similarity:", e)
            max_emb = 0

        is_hallucinated = (max_seq < self.threshold) and (max_emb < self.emb_threshold)
        self.last_scores = {"string_sim": round(max_seq, 2), "embedding_sim": round(max_emb, 2)}
        return is_hallucinated

    def explain(self, context: str, answer: str) -> str:
        if not context or not answer:
            return "ℹ️ No source context or answer, confidence score cannot be calculated."
        result = self.is_hallucinated(context, answer)
        sim, emb = self.last_scores["string_sim"], self.last_scores["embedding_sim"]
        if result:
            return (f"⚠️ The answer DOES NOT MATCH the source!\n"
                    f"(String similarity: {sim}, Embedding similarity: {emb})")
        else:
            return (f"✅ The answer is consistent with the source.\n"
                    f"(String similarity: {sim}, Embedding similarity: {emb})")

def hallucination_node(state):
    node = HallucinationChecker()
    context = state.get("context", "")
    answer = state.get("answer", "")
    explanation = node.explain(context, answer)
    state["hallucination"] = explanation
    return state
