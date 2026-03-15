import os
import hashlib
from datetime import datetime, timedelta
import pytz

from dotenv import load_dotenv
from serpapi import GoogleSearch
from livekit.agents.llm import function_tool

from logger import logger

load_dotenv(".env.local")

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

if not SERPAPI_KEY:
    logger.error("SERPAPI_KEY not found in environment variables")

# ==============================
# CACHE
# ==============================

search_cache = {}
CACHE_TTL = 600


def _generate_cache_key(query: str) -> str:
    return hashlib.md5(query.lower().strip().encode()).hexdigest()


def _is_cache_valid(entry):
    return datetime.utcnow() < entry["expiry"]


# ==============================
# SEARCH TOOL
# ==============================

@function_tool(
    name="search",
    description="Search the internet for real-time information such as news, weather, and current events."
)
async def search(query: str, num_results: int = 3) -> dict:

    cache_key = _generate_cache_key(query)

    if cache_key in search_cache and _is_cache_valid(search_cache[cache_key]):
        logger.info(f"CACHE_HIT | {query}")

        cached = search_cache[cache_key]["data"]

        return {
            **cached,
            "results": cached["results"][:num_results],
            "results_count": min(len(cached["results"]), num_results),
            "cached": True
        }

    logger.info(f"SEARCH_START | Query: {query}")

    try:

        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": min(num_results, 10)
        }

        search_client = GoogleSearch(params)
        data = search_client.get_dict()

        organic_results = data.get("organic_results", [])

        if not organic_results:

            logger.warning(f"NO_RESULTS | {query}")

            return {
                "status": "no_results",
                "query": query,
                "message": f"No results found for '{query}'"
            }

        results = [
            {
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")
            }
            for item in organic_results[:num_results]
        ]

        result_data = {
            "status": "success",
            "query": query,
            "results_count": len(results),
            "results": results,
            "cached": False
        }

        search_cache[cache_key] = {
            "data": result_data,
            "expiry": datetime.utcnow() + timedelta(seconds=CACHE_TTL)
        }

        logger.info(f"SEARCH_SUCCESS | {query}")

        return result_data

    except Exception as e:

        logger.error(f"SEARCH_ERROR | {query} | {str(e)}")

        return {
            "status": "error",
            "query": query,
            "message": str(e)
        }


# ==============================
# TOOL LOADER
# ==============================

def get_search_tool():
    logger.info("NEMU Search Engine initialized")
    return search


# ==============================
# TIME TOOL
# ==============================

@function_tool(
    name="get_current_time",
    description="Get the current time in Indian Standard Time"
)
async def get_current_time() -> str:

    ist = pytz.timezone("Asia/Kolkata")
    now = datetime.now(ist)

    return now.strftime("%A, %d %B %Y, %I:%M:%S %p IST")
