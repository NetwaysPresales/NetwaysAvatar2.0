import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_REALTIME_ENDPOINT = os.getenv("AZURE_OPENAI_REALTIME_ENDPOINT")
AZURE_OPENAI_REALTIME_KEY = os.getenv("AZURE_OPENAI_REALTIME_KEY")

AZURE_AI_SEARCH_ENDPOINT = os.environ["AZURE_AI_SEARCH_ENDPOINT"]
AZURE_AI_SEARCH_INDEX = os.environ["AZURE_AI_SEARCH_INDEX"]
AZURE_AI_SEARCH_KEY = os.environ["AZURE_AI_SEARCH_KEY"]
AZURE_AI_SEARCH_SEMANTIC_CONFIG = os.environ["AZURE_AI_SEARCH_SEMANTIC_CONFIG"]

TAVILY_KEY = os.getenv("TAVILY_KEY")