
import gradio as gr
from agent import shopgenie_agent


# Chat function
def chat(message, history):
    try:
        answer = shopgenie_agent(message)
        return answer

    except Exception as e:
        return f"Error: {str(e)}"


# Create Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title="ShopGenie AI Assistant",
    description=(
        "Your AI shopping assistant powered by "
        "Qwen LLM, LangChain and Ollama."
    ),
    examples=[
        "Find Laptop A specifications",
        "Compare Laptop A and Laptop B",
        "What is the price of Laptop C?",
        "Which laptop has 16GB RAM?"
    ]
)


# Launch application
if __name__ == "__main__":
    demo.launch()
