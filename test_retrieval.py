
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# Connect to embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)


# Load existing vector database
vectorstore = Chroma(
    collection_name="shopgenie_products",
    embedding_function=embeddings,
    persist_directory="./vector_db"
)


# Ask a question
query = "Which laptop has 16GB RAM?"


# Search similar documents
results = vectorstore.similarity_search(
    query,
    k=3
)


# Display retrieved documents
print("User Query:", query)

print("\nRetrieved Documents:")

for i, doc in enumerate(results):
    print(f"\nResult {i+1}:")
    print(doc.page_content)
