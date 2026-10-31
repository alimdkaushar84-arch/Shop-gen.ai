
import os
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

print("Current folder:", os.getcwd())

embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    collection_name="shopgenie_products",
    embedding_function=embeddings,
    persist_directory="./vector_db"
)

print("Stored documents:", db._collection.count())

results = db.similarity_search(
    "Laptop price and RAM",
    k=3
)

print("\nRetrieved documents:")

for doc in results:
    print("-------------------")
    print(doc.page_content)
