

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from ingestion import load_and_split_documents

print("Loading documents...")

chunks = load_and_split_documents()

print("Total chunks:", len(chunks))

print("Creating embeddings...")

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

print("Storing documents in ChromaDB...")

vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="shopgenie_products",
    persist_directory="./vector_db"
)

print("Documents stored successfully!")

print("Stored count:", vectorstore._collection.count())
