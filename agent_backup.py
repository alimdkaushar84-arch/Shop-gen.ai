

# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, ToolMessage

# from tools.shop_tools import (
#     product_search,
#     compare_prices,
#     rag_search
# )


# # 1. Load LLM
# llm = ChatOllama(
#     model="qwen2.5:3b",
#     temperature=0
# )

# # 2. Register tools
# tools = [
#     product_search,
#     compare_prices,
#     rag_search
# ]
# # Create tool mapping
# tool_map = {
#     tool.name: tool
#     for tool in tools
# }


# llm_with_tools = llm.bind_tools(tools)


# # 3. Create agent function
# def shopgenie_agent(question):

#     messages = [
#         HumanMessage(content=question)
#     ]

#     # Ask LLM to decide whether a tool is needed
#     response = llm_with_tools.invoke(messages)

#     messages.append(response)

#     # Execute requested tools
#     for tool_call in response.tool_calls:

#         tool_name = tool_call["name"]
#         arguments = tool_call["args"]

#         print("\nAction:", tool_name)

#         result = tool_map[tool_name].invoke(arguments)

#         print("Observation:", result)

#         messages.append(
#             ToolMessage(
#                 content=str(result),
#                 tool_call_id=tool_call["id"]
#             )
#         )

#     # 4. Generate final answer
#     final_response = llm.invoke(messages)

#     return final_response.content


# # 5. Test agent
# if __name__ == "__main__":

#     print("Welcome to ShopGenie AI!")

#     while True:

#         question = input("\nYou: ")

#         if question.lower() == "exit":
#             break

#         answer = shopgenie_agent(question)

#         print("\nShopGenie:", answer)

# from langchain_ollama import ChatOllama
# from langchain_core.messages import HumanMessage, ToolMessage

# from tools.shop_tools import (
#     product_search,
#     compare_prices,
#     rag_search
# )

# # 1. Load LLM
# llm = ChatOllama(
#     model="qwen2.5:3b",
#     temperature=0
# )

# # 2. Register tools
# tools = [
#     product_search,
#     compare_prices,
#     rag_search
# ]

# # 3. Create tool mapping
# tool_map = {
#     tool.name: tool
#     for tool in tools
# }

# # 4. Connect tools to LLM
# llm_with_tools = llm.bind_tools(tools)


# # 5. Agent function
# def shopgenie_agent(question, history=None):

#     messages = []

#     # Add previous conversation
#     if history:
#         for item in history:
#             if isinstance(item, dict):
#                 if item.get("role") == "user":
#                     messages.append(
#                         HumanMessage(content=item["content"])
#                     )

#     messages.append(HumanMessage(content=question))

#     # Allow multiple tool-calling rounds
#     for step in range(5):

#         response = llm_with_tools.invoke(messages)
#         messages.append(response)

#         if not response.tool_calls:
#             return response.content

#         for tool_call in response.tool_calls:

#             tool_name = tool_call["name"]
#             arguments = tool_call["args"]

#             print("\nAction:", tool_name)

#             result = tool_map[tool_name].invoke(arguments)

#             print("Observation:", result)

#             messages.append(
#                 ToolMessage(
#                     content=str(result),
#                     tool_call_id=tool_call["id"]
#                 )
#             )

#     return "I could not complete the request within the tool-call limit."


# # 6. Test agent
# if __name__ == "__main__":

#     print("Welcome to ShopGenie AI!")

#     while True:

#         question = input("\nYou: ")

#         if question.lower() == "exit":
#             break

#         answer = shopgenie_agent(question)

#         print("\nShopGenie:", answer)

from langchain_ollama import ChatOllama
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

from tools.shop_tools import (
    product_search,
    compare_prices,
    rag_search
)

# Load LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.3
)

# Register tools
tools = [
    product_search,
    compare_prices,
    rag_search
]

tool_map = {
    tool.name: tool for tool in tools
}

llm_with_tools = llm.bind_tools(tools)

# Instructions for ShopGenie
system_prompt = """
You are ShopGenie, a general AI shopping assistant.

You can answer general questions about:
- Laptops and computers
- Mobile phones
- Headphones
- Electronics
- Shopping advice
- Product comparisons
- Technology

IMPORTANT RULES:

1. Answer general questions directly using your knowledge.
2. Use product_search for products in the shop catalogue.
3. Use compare_prices for comparing products in the shop catalogue.
4. Use rag_search for questions about stored product policies
   and warranty information.
5. Do not invent product prices, stock availability,
   warranties or shop-specific information.
6. If information is unavailable, clearly tell the user.
7. Give simple, helpful and understandable answers.
"""

# Agent function
def shopgenie_agent(question, history=None):

    messages = [
        SystemMessage(content=system_prompt)
    ]

    # Preserve previous conversation
    if history:
        for item in history:
            if not isinstance(item, dict):
                continue

            role = item.get("role")
            content = item.get("content", "")

            if not isinstance(content, str):
                continue

            if role == "user":
                messages.append(HumanMessage(content=content))

            elif role == "assistant":
                messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=question))

    # ReAct-style tool execution
    for step in range(5):

        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool is needed, answer directly
        if not response.tool_calls:
            return response.content

        # Execute selected tools
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            arguments = tool_call["args"]

            print("\nAction:", tool_name)

            if tool_name not in tool_map:
                result = "Requested tool is unavailable."
            else:
                result = tool_map[tool_name].invoke(arguments)

            print("Observation:", result)

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return "Please try asking your question in a simpler way."


if __name__ == "__main__":

    print("Welcome to ShopGenie!")

    while True:

        question = input("\nYou: ")

        if question.lower() == "exit":
            break

        answer = shopgenie_agent(question)

        print("\nShopGenie:", answer)
