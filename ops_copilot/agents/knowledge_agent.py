from ops_copilot.rag.rag_chain import answer_with_rag


def kb_search(query: str) -> str:
    """
    Query the Ops knowledge base using RAG.
    """
    return answer_with_rag(query)
