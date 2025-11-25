from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.chains import RetrievalQA

from ops_copilot.config import GEMINI_API_KEY, DEFAULT_MODEL
from ops_copilot.rag.vectordb import load_vectorstore


def build_rag_chain():
    vectordb = load_vectorstore()
    retriever = vectordb.as_retriever(search_kwargs={"k": 4})

    llm = ChatGoogleGenerativeAI(
        model=DEFAULT_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.1,
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False,
    )
    return chain


def answer_with_rag(query: str) -> str:
    chain = build_rag_chain()
    result = chain({"query": query})
    return result["result"]
