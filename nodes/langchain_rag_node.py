from langchain_community.llms import OpenAI
from langchain_community.document_loaders import WikipediaLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import os

class LangChainRAGNode:
    def __init__(self, language="en"):
        self.language = language
        self.llm = OpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.4,
        )

    def run(self, user_query):
        try:
            docs = WikipediaLoader(query=user_query, lang=self.language).load()
            context = docs[0].page_content if docs else ""
        except Exception as e:
            print("[LangChainRAGNode] Wikipedia error:", e)
            context = ""

        prompt = PromptTemplate(
            template="Question: {question}\nContext: {context}\nAnswer:",
            input_variables=["question", "context"]
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.invoke({"question": user_query, "context": context})
        return response["text"]

def langchain_rag_node(state):
    node = LangChainRAGNode(language=state.get("language", "tr"))
    context = node.run(state.get("user_input", ""))
    state["context"] = context
    return state
