
from langchain_core.tools import tool
from rag_tool import ask_shopgenie


@tool
def rag_search(question: str) -> str:
    """
    Search stored documents for product information,
    warranty details, return policies and other policies.
    """

    try:
        answer = ask_shopgenie(question)
        return str(answer)

    except Exception as e:
        return f"Document search error: {e}"
