from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_knowledge_base(path: str = "data/knowledge_base"):
    base = Path(path)
    docs = []
    for file in base.glob("**/*"):
        if file.is_file() and file.suffix.lower() in [".md", ".txt"]:
            docs.extend(TextLoader(str(file), encoding="utf-8").load())
    return docs


def split_docs(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )
    return splitter.split_documents(docs)
