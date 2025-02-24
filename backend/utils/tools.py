import config
from tavily import TavilyClient
tavily_client = TavilyClient(api_key=config.TAVILY_KEY)

def search_web(query: str):
    """
    Web search based on query.
    """
    response = tavily_client.search(query)
    return response

def search_data():
    """
    Searches through data in Azure AI Search.
    """
    with open("C:/Users/me/Desktop/Netways/NetwaysAvatar2.0/backend/utils/Dubai_Racing_Club.md", "r", encoding="utf-8") as file:
        return file.read()

def fetch_user_from_db(user_id: str):
    """
    Fetches user data from the database.
    Returns a dictionary with user details if found, else None.
    """
    # Simulated database query
    mock_db = {
        "1234": {
            "name": "Alice Example",
            "job": "Software Engineer",
            "past_conversations": [
                {"id": "conv1", "title": "Chat from Jan 1", "summary": "Summary of chat 1"},
                {"id": "conv2", "title": "Chat from Feb 5", "summary": "Summary of chat 2"}
            ]
        },
        "5678": {
            "name": "Bob AI",
            "job": "Data Scientist",
            "past_conversations": [
                {"id": "conv3", "title": "Research Chat", "summary": "Discussed AI papers"},
                {"id": "conv4", "title": "ML Talk", "summary": "Spoke about deep learning"}
            ]
        }
    }

    return mock_db.get(user_id, None)
