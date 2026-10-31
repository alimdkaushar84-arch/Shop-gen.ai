
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Load embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# 2. Connect to existing ChromaDB
vectorstore = Chroma(
    collection_name="shopgenie_products",
    embedding_function=embeddings,
    persist_directory="./vector_db"
)

# 3. Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 4. Load local LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# 5. Create prompt
prompt = ChatPromptTemplate.from_template("""
You are ShopGenie, an AI shopping assistant.

Answer the user's question using only the given context.

If the answer is not available in the context,
say that the information is not available.

Context:
{context}

Question:
{question}

Answer:
""")

# 6. Format retrieved documents
def format_docs(docs):
    return "\n\n".join(
        doc.page_content for doc in docs
    )

# 7. Create RAG function
def ask_shopgenie(question):

    # Retrieve relevant documents
    docs = retriever.invoke(question)

    if not docs:
        return "Sorry, no relevant information was found."

    # Prepare context
    context = format_docs(docs)

    # Generate answer
    rag_chain = prompt | llm | StrOutputParser()

    answer = rag_chain.invoke({
        "context": context,
        "question": question
    })

    return answer


# 8. Test the RAG system
if __name__ == "__main__":

    question = input("Ask ShopGenie: ")

    answer = ask_shopgenie(question)

    print("\nShopGenie Answer:")
    print(answer)
