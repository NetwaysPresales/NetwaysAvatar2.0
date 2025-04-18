import config
from logger import logger
from tavily import TavilyClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

tavily_client = TavilyClient(api_key=config.TAVILY_KEY)
ai_search_client = SearchClient(endpoint=config.AZURE_AI_SEARCH_ENDPOINT,
                                index_name=config.AZURE_AI_SEARCH_INDEX,
                                credential=AzureKeyCredential(config.AZURE_AI_SEARCH_KEY))

def search_web(query: str):
    """
    Web search based on query.
    """
    try:
        response = tavily_client.search(query)
        logger.info("Successfully called Tavily web search with query: %s", query)

        return "\n\n".join([result.get("content") for result in response.get("results")])
    except Exception as e:
        logger.error("Error calling Tavily web search with query: %s", query)

def search_data(query: str):
    """
    Searches through data in Azure AI Search.
    """
    try:
        responses =  ai_search_client.search(query_type='semantic', semantic_configuration_name=config.AZURE_AI_SEARCH_SEMANTIC_CONFIG,
                                        search_text=query, select='chunk', query_caption='extractive')
        logger.info("Successfully called Azure AI Search with query: %s", query)
        
        result = "AI Search Result: \n\n"
        for i, response in enumerate(responses):
            result += f"Chunk {i+1}: \n\n" + response['chunk'] + "\n\n" 

        # print(result)

        return result
    except Exception as e:
        logger.error("Error calling Azure AI Search with query: %s", query)

def get_ticket_prices():
    """
    Returns a .md file containing all the ticket prices and details retreived from website. 
    """
    try:
        with open("C:/Users/me/Desktop/Work/Netways/NetwaysAvatar2.0/backend/utils/DRC_Ticket_Pricing_Data.md") as file:
            text = file.read()

            logger.info("Successfully retreived ticket data")

            return text
    except Exception as e:
        logger.error("Error retreiving ticket data")

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
