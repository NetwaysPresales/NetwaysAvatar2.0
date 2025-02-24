import os
from dotenv import load_dotenv

load_dotenv()

AZURE_OPENAI_REALTIME_ENDPOINT = os.getenv("AZURE_OPENAI_REALTIME_ENDPOINT")
AZURE_OPENAI_REALTIME_KEY = os.getenv("AZURE_OPENAI_REALTIME_KEY")
TAVILY_KEY = os.getenv("TAVILY_KEY")