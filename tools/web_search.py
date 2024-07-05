import json
import os

from langchain_community.utilities import BingSearchAPIWrapper
from langchain_core.tools import tool

BING_API_KEY = os.getenv("BING_API_KEY")

search_api = BingSearchAPIWrapper(bing_subscription_key=BING_API_KEY)

@tool
def web_search(query: str) -> str:
    """Search information online using search engine"""
    results = search_api.results(query, 10)
    return json.dumps(results)

