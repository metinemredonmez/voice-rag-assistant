from fastapi import FastAPI, Body
from nodes.gpt_node import GPTNode
from nodes.rag_node import RAGNode

app = FastAPI()
gpt = GPTNode(language="en")
rag = RAGNode(language="en")

@app.post("/ask")
def ask_ai(question: str = Body(...)):
    """
    AI Assistant: Receives a question, retrieves context from Wikipedia, and answers with GPT.
    """
    context = rag.run(question)
    answer = gpt.run(question, context=context)
    return {"question": question, "context": context, "answer": answer}
