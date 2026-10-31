from langchain_ollama import ChatOllama

# Connect to local Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)
question=input("what can i help you")
# Send a message
response = llm.invoke(question)

# Print response
print(response.content)