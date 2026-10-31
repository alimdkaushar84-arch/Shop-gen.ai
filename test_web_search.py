from tools.web_search_tool import web_search

result = web_search.invoke({
    "query": "Best laptops under 60000 in India"
})

print(result)