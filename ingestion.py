
from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)


from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader
)

from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_documents():

    data_path = Path("data")
    documents = []

    # Load TXT files
    for file_path in data_path.glob("*.txt"):
        loader = TextLoader(
            str(file_path),
            encoding="utf-8"
        )
        documents.extend(loader.load())

    # Load PDF files
    for file_path in data_path.glob("*.pdf"):
        loader = PyPDFLoader(str(file_path))
        documents.extend(loader.load())

    if not documents:
        raise ValueError("No documents found in data folder.")

    print("Documents loaded:", len(documents))

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(documents)

    print("Total chunks:", len(chunks))

    return chunks


if __name__ == "__main__":
    chunks = load_and_split_documents()

    for i, chunk in enumerate(chunks):
        print(f"\n--- CHUNK {i+1} ---")
        print(chunk.page_content)
