
from langchain_ollama import ChatOllama

try:
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0
    )

    response = llm.invoke(
        "What is artificial intelligence?"
    )

    print("LLM is working!")
    print(response.content)

except Exception as e:
    print("LLM ERROR:")
    print(repr(e))
