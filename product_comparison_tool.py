
# from ddgs import DDGS
# from langchain_core.tools import tool

# # General shopping platforms that cover many product categories
# SHOPPING_PLATFORMS = {
#     "Amazon India": "amazon.in",
#     "Flipkart": "flipkart.com",
#     "Meesho": "meesho.com",
#     "Snapdeal": "snapdeal.com",
#     "Tata CLiQ": "tatacliq.com",
#     "JioMart": "jiomart.com",
# }


# @tool
# def product_comparison_search(query: str) -> str:
#     """
#     Search for any product across general shopping platforms
#     and the wider internet.

#     Supports all product categories without predefined
#     category restrictions.
#     """

#     output = []

#     try:
#         with DDGS() as ddgs:

#             # Search the wider internet
#             output.append("========== GENERAL WEB SEARCH ==========")

#             results = ddgs.text(query + " India", max_results=5)

#             if results:
#                 for result in results:
#                     output.append(
#                         f"Title: {result.get('title', 'N/A')}\n"
#                         f"Description: {result.get('body', 'N/A')}\n"
#                         f"Link: {result.get('href', 'N/A')}"
#                     )
#             else:
#                 output.append("No general results found.")

#             # Search shopping platforms
#             for platform, domain in SHOPPING_PLATFORMS.items():

#                 output.append(f"\n========== {platform} ==========")

#                 try:
#                     results = ddgs.text(
#                         f"site:{domain} {query}",
#                         max_results=3
#                     )

#                     if results:
#                         for result in results:
#                             output.append(
#                                 f"Title: {result.get('title', 'N/A')}\n"
#                                 f"Description: {result.get('body', 'N/A')}\n"
#                                 f"Link: {result.get('href', 'N/A')}"
#                             )
#                     else:
#                         output.append("No results found.")

#                 except Exception as e:
#                     output.append(f"Search failed: {e}")

#     except Exception as e:
#         return f"Internet search unavailable: {e}"

#     return "\n\n".join(output)


# if __name__ == "__main__":
#     user_question = input("Enter your product query: ")

#     result = product_comparison_search.invoke({
#         "query": user_question
#     })

#     print("\nSHOPGENIE RESULTS\n")
#     print(result)


# from ddgs import DDGS
# from langchain_core.tools import tool


# @tool
# def product_comparison_search(query: str) -> str:
#     """
#     Search the internet for products across different
#     categories, brands and shopping platforms.

#     Returns product details, shopping links and
#     available product images.
#     """

#     output = []

#     try:
#         with DDGS() as ddgs:

#             # Search for product information
#             output.append("========== PRODUCT SEARCH RESULTS ==========")

#             try:
#                 text_results = list(
#                     ddgs.text(
#                         query + " India",
#                         max_results=5
#                     )
#                 )

#                 if text_results:
#                     for i, result in enumerate(text_results, 1):

#                         output.append(
#                             f"\nProduct Result {i}\n"
#                             f"Title: {result.get('title', 'Not available')}\n"
#                             f"Description: {result.get('body', 'Not available')}\n"
#                             f"Source: {result.get('href', 'Not available')}"
#                         )

#                 else:
#                     output.append("No product information found.")

#             except Exception as e:
#                 output.append(f"Product search error: {e}")

#             # Search for product images
#             output.append("\n========== PRODUCT IMAGES ==========")

#             try:
#                 image_results = list(
#                     ddgs.images(
#                         query + " product image",
#                         max_results=5
#                     )
#                 )

#                 if image_results:

#                     for i, result in enumerate(image_results, 1):

#                         image_url = result.get("image")
#                         image_title = result.get("title", "Product image")
#                         source_url = result.get("url", "")

#                         if image_url and image_url.startswith(("http://", "https://")):

#                             output.append(
#                                 f"\nImage {i}\n"
#                                 f"![{image_title}]({image_url})\n"
#                                 f"Image source: {source_url}"
#                             )

#                 else:
#                     output.append("No product images found.")

#             except Exception as e:
#                 output.append(f"Image search error: {e}")

#     except Exception as e:
#         return f"Internet search unavailable: {str(e)}"

#     return "\n\n".join(output)


# # Test the tool independently
# if __name__ == "__main__":

#     user_query = input("Enter product name or question: ")

#     result = product_comparison_search.invoke(
#         {"query": user_query}
#     )

#     print("\nShopGenie Search Results:")
#     print(result)

from ddgs import DDGS
from langchain_core.tools import tool


# Indian shopping platforms
PLATFORMS = {
    "Amazon India": "amazon.in",
    "Flipkart": "flipkart.com",
    "Croma": "croma.com",
    "Reliance Digital": "reliancedigital.in",
    "Tata CLiQ": "tatacliq.com",
    "Vijay Sales": "vijaysales.com",
    "Myntra": "myntra.com",
    "AJIO": "ajio.com",
}


@tool
def product_comparison_search(query: str) -> str:
    """
    Find individual products across Indian shopping platforms.
    Retrieve product descriptions, prices, specifications,
    source links and available product images.
    Supports any product category.
    """

    output = []
    seen_urls = set()

    try:
        with DDGS() as ddgs:

            output.append("SHOPGENIE PRODUCT DISCOVERY")
            output.append(f"User request: {query}")
            output.append("Shopping region: India")
            output.append("Currency: INR")

            # Search individual shopping platforms
            for platform, domain in PLATFORMS.items():

                output.append(f"\n\n===== {platform} =====")

                try:
                    search_query = (
    f"site:{domain} {query} India "
    "price features specifications buy online"
)

                    results = list(
                        ddgs.text(
                            search_query,
                            max_results=3
                        )
                    )

                    valid_results = 0

                    for item in results:

                        url = item.get("href", "")

                        if not url or url in seen_urls:
                            continue

                        seen_urls.add(url)
                        valid_results += 1

                        output.append(
                            f"\nProduct result {valid_results}\n"
                            f"Name: {item.get('title', 'Unavailable')}\n"
                            f"Details: {item.get('body', 'Unavailable')}\n"
                            f"Platform: {platform}\n"
                            f"Product link: {url}\n"
                            f"Buy Product: {url}\n"
                            "Price: Verify on product page\n"
                            "Specifications: Check source"
                        )

                    if valid_results == 0:
                        output.append(
                            "No verified search results returned "
                            "for this platform."
                        )

                except Exception as e:
                    output.append(
                        f"Platform search unavailable: {e}"
                    )

            # General web search for additional product information
            output.append("\n\n===== ADDITIONAL PRODUCT INFORMATION =====")

            try:
                results = list(
                    ddgs.text(
                        f"{query} India price specifications review",
                        max_results=5
                    )
                )

                for item in results:

                    url = item.get("href", "")

                    if url and url not in seen_urls:
                        seen_urls.add(url)

                        output.append(
                            f"\nTitle: {item.get('title', 'Unavailable')}\n"
                            f"Details: {item.get('body', 'Unavailable')}\n"
                            f"Source: {url}"
                        )

            except Exception as e:
                output.append(f"Additional search error: {e}")

            # Search for product pictures
            output.append("\n\n===== PRODUCT IMAGES =====")

            try:
                images = list(
                    ddgs.images(
                        f"{query} product India",
                        max_results=6
                    )
                )

                for item in images:

                    image_url = item.get("image")
                    image_title = item.get(
                        "title", "Product image"
                    )

                    if image_url and image_url.startswith("https://"):

                        output.append(
                            f"\nImage title: {image_title}\n"
                            f"Image URL: {image_url}\n"
                            f"Source: {item.get('url', 'Unavailable')}"
                        )

                if not images:
                    output.append("No images found.")

            except Exception as e:
                output.append(f"Image search error: {e}")

    except Exception as e:
        return f"Product discovery failed: {e}"

    return "\n".join(output)


if __name__ == "__main__":

    query = input("What product are you looking for? ")

    result = product_comparison_search.invoke(
        {"query": query}
    )

    print("\n", result)
