

# from langchain_ollama import ChatOllama

# from tools.shop_tools import rag_search
# from tools.web_search_tool import web_search
# from tools.product_comparison_tool import product_comparison_search


# # Load local LLM
# llm = ChatOllama(
#     model="qwen2.5:3b",
#     temperature=0
# )


# # Register available tools
# tools = [
#     rag_search,
#     web_search,
#     product_comparison_search
# ]

# tool_map = {tool.name: tool for tool in tools}

# # Connect tools to LLM
# llm_with_tools = llm.bind_tools(tools)


# # Accept any natural-language question
# question = input("Enter your question: ")

# response = llm_with_tools.invoke(question)

# print("\nAI Response:")
# print(response.content)


# # Check whether a tool was selected
# if response.tool_calls:

#     for tool_call in response.tool_calls:

#         tool_name = tool_call["name"]
#         arguments = tool_call["args"]

#         print("\nTool selected:", tool_name)
#         print("Arguments:", arguments)

#         if tool_name in tool_map:

#             selected_tool = tool_map[tool_name]

#             result = selected_tool.invoke(arguments)

#             print("\nTool Result:")
#             print(result)

#         else:
#             print("Tool not available.")

# else:
#     print("No tool was selected.")

from langchain_core.tools import tool
from rag_tool import ask_shopgenie


@tool
def rag_search(question: str) -> str:
    """Search stored documents and policies."""

    try:
        return str(ask_shopgenie(question))

    except Exception as e:
        return f"Document search error: {e}"
