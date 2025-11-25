from ops_copilot.rag.loader import load_knowledge_base, split_docs
from ops_copilot.rag.vectordb import build_vectorstore

if __name__ == "__main__":
    docs = load_knowledge_base()
    print("Loaded docs:", len(docs))

    chunks = split_docs(docs)
    print("Chunks:", len(chunks))

    build_vectorstore(chunks)
    print("Vectorstore built successfully!")
