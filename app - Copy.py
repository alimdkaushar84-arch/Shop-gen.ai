

# import gradio as gr
# from agent import shopgenie_agent


# # Chat function
# def chat(message, history):
#     try:
#         answer = shopgenie_agent(message, history)
#         return answer

#     except Exception as e:
#         return f"Error: {str(e)}"


# # Create Gradio interface
# # demo = gr.ChatInterface(
# #     fn=chat,
# #     title="ShopGenie",
# #     description="Hii! Welcome to ShopGenie. Your AI shopping assistant. Ask me anything!"
# # 
# # )
# def chat(message, history):
#     try:
#         return shopgenie_agent(message, history)
#     except Exception as e:
#         return f"Error: {e}"

# # Launch application
# if __name__ == "__main__":
#     demo.launch()



import gradio as gr
from agent import shopgenie_agent


def chat(message, history):
    try:
        return shopgenie_agent(message, history)
    except Exception as e:
        return f"Error: {e}"


with gr.Blocks() as demo:

    gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>Welcome to ShopGenie!</h1>
            <h3>Your AI Shopping Assistant</h3>
            <p>Find products, compare prices and get smart recommendations.</p>
        </div>
    """)

    gr.ChatInterface(
        fn=chat
    )


if __name__ == "__main__":
    demo.launch()
