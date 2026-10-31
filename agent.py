
from langchain_ollama import ChatOllama

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage
)

from tools.shop_tools import rag_search
from tools.web_search_tool import web_search
from tools.product_comparison_tool import product_comparison_search


# 1. Initialize LLM
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.3
)


# 2. Register tools
tools = [
    rag_search,
    web_search,
    product_comparison_search
]

tool_map = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)


# 3. ShopGenie System Prompt
system_prompt = """
You are ShopGenie, a general-purpose AI assistant
with universal shopping capabilities.

GENERAL CONVERSATION:
- Answer any general question naturally.
- Help with coding, education and explanations.
- Do not use tools unnecessarily.

UNIVERSAL SHOPPING:
- Support every product category and brand.
- Understand natural-language shopping requests.
- Search online for products, prices and specifications.
- Compare products across shopping platforms.
- Never restrict searches to predefined categories.
- Use product_comparison_search for online shopping.

RAG:
- Use rag_search for stored documents and policies.

WEB RESEARCH:
- Use web_search for general internet research.

IMPORTANT:
- Do not use the old sample laptop database.
- Do not invent prices, ratings or specifications.
- Pass the user's actual question to the appropriate tool.
- Include available source links in shopping answers.
- If no tool is required, answer directly.
- Remember relevant conversation history.
PRODUCT DISCOVERY:
- Search for individual products across different platforms.
- Display each product separately.
- Include the platform name and product source link.
- Include available prices and specifications.
- Do not invent missing product information.
- Use INR for Indian shopping searches.

PRODUCT CONVERSATION:
- Remember products found in previous messages.
- Answer follow-up questions about those products.
- Compare processors, RAM, storage, battery and other features.
- Explain advantages and disadvantages.
- Recommend products based on the user's requirements.
- Search again if required information is missing.
- Preserve available product image Markdown.
"""


# 4. Main ShopGenie Agent
def shopgenie_agent(question, history=None):

    messages = [
        SystemMessage(content=system_prompt)
    ]

    # Add conversation history
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

    # 5. ReAct-style tool execution loop
    for step in range(5):

        response = llm_with_tools.invoke(messages)

        messages.append(response)

        # Return direct answer if no tool is needed
        if not response.tool_calls:
            return response.content

        # Execute selected tools
        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]
            arguments = tool_call["args"]

            print("\nAction:", tool_name)

            if tool_name in tool_map:

                try:
                    result = tool_map[tool_name].invoke(arguments)

                except Exception as e:
                    result = f"Tool execution error: {e}"

            else:
                result = "Requested tool is unavailable."

            print("Observation:", result)

            # Send tool result back to LLM
            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

    return "I could not complete the request. Please try again."


# 6. Run ShopGenie in terminal
if __name__ == "__main__":

    print("================================")
    print("       Welcome to ShopGenie")
    print("================================")

    while True:

        question = input("\nYou: ")

        if question.lower().strip() in ["exit", "quit"]:
            print("ShopGenie closed.")
            break

        answer = shopgenie_agent(question)

        print("\nShopGenie:", answer)


