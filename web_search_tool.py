from ddgs import DDGS
from langchain_core.tools import tool


@tool
def web_search(query: str) -> str:
    """Search the internet for current product information,
    prices, specifications, brands and shopping comparisons."""

    try:
        results = DDGS().text(query, max_results=5)

        if not results:
            return "No relevant search results found."

        output = []

        for i, result in enumerate(results, start=1):
            output.append(
                f"Result {i}\n"
                f"Title: {result.get('title', 'N/A')}\n"
                f"Description: {result.get('body', 'N/A')}\n"
                f"Link: {result.get('href', 'N/A')}"
            )

        return "\n\n".join(output)

    except Exception as e:
        return f"Web search error: {str(e)}"