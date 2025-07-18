import os
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY") or None

if not TAVILY_API_KEY:
    raise NotImplementedError("TAVILY_API_KEY is not set")

tavily_search = TavilySearch(api_key=TAVILY_API_KEY)

@tool
def web_search(query: str, config: RunnableConfig) -> str:
    """Search the web for the most relevant information."""
    try:
        print(f"Web Search Config: {config}")
        response = tavily_search.invoke({"query": query})

        if isinstance(response, dict) and "results" in response:
            formatted_results = []
            for item in response['results']:
                title = item.get('title', 'No title')
                url = item.get('url', '')
                content = item.get('content', 'No content')
                formatted_results.append(f"Title: {title}\nContent: {content}\nURL: {url}\n")

            return "\n\n".join(formatted_results) if formatted_results else "No results found"
        else:
            return str(response)
    except Exception as e:
        return f"Web Error: {str(e)}"