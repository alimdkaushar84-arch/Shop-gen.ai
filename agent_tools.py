from langchain_core.tools import tool

@tool
def calculate_discount(price: float, discount: float) -> str:
    """Calculate the final price after applying a percentage discount."""

    final_price = price - (price * discount / 100)

    return f"Final price after discount: Rs. {final_price:.2f}"


# Test the tool directly
result = calculate_discount.invoke({
    "price": 2000,
    "discount": 15
})

print(result)