from ops_copilot.rag.rag_chain import answer_with_rag

if __name__ == "__main__":
    q = "What should the daily Ops report include?"
    print("Q:", q)
    print("A:", answer_with_rag(q))
