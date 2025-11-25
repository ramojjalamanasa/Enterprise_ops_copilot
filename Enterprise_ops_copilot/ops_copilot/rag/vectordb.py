from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

PERSIST_DIR = "chroma_db"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


def build_vectorstore(chunks, persist_directory: str = PERSIST_DIR):
    embeddings = get_embeddings()

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=persist_directory,
    )
    # No explicit persist() in langchain_chroma.Chroma
    # Data is stored in the given persist_directory automatically.
    return vectordb


def load_vectorstore(persist_directory: str = PERSIST_DIR):
    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
    return vectordb
