from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class Tool(BaseModel):
    """Represents an individual tool that can be enabled for AI functionality."""
    type: str
    name: str
    description: Optional[str] = None
    parameters: Optional[dict] = None

    def to_json(self):
        return {
            "type": self.type,
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters
        }

search_data_tool = Tool(
    type="function",
    name="search_data",
    description="""Searches content using Azure AI Search based on the parameter 'query', and returns the results as text. 
    Contains information regarding Dubai Racing Club condition book, events, private suite menu items, and ticket details. 
    Always prioritize this function over the web_search function for Dubai Racing Club information.
    """,
    parameters={
        "type": "object",
        "properties": {
            "query": { "type": "string" }
        },
        "required": ["query"]
    }
)

web_search_tool = Tool(
    type="function",
    name="search_web",
    description="""Conducts a web search based on the parameter 'query', and returns the results from the web. 
    Can be used to search for any information that you do not know.
    
    
    استخدم هذه الدالة للبحث في الويب عندما تحتاج إلى معلومات لا تمتلكها.""",
    parameters={
        "type": "object",
        "properties": {
            "query": { "type": "string" }
        },
        "required": ["query"]
    }
)

get_ticket_prices_tool = Tool(
    type="function",
    name="get_ticket_prices",
    description="""Retreives official prices for tickets, including suite tickets and other types of tickets as well.
    Always run this function if ticket pricing information is asked by the user.
    """,
    parameter=None
)

class OpenAIConfig(BaseModel):
    """Settings related to OpenAI model behavior and processing."""
    model: str = "gpt-4o-realtime-preview"
    voice: str = "alloy"
    temperature: float = Field(0.8, ge=0.0, le=1.0)  # AI creativity level (0-1)
    max_tokens: int = Field(2000, gt=0)  # Maximum tokens per response
    enable_streaming: bool = True  # Whether responses are streamed

class PTTConfig(BaseModel):
    """Settings related to the Push-to-Talk (PTT)."""
    button: str = "space"
    stream_input: bool = False

class VADConfig(BaseModel):
    """Settings related to Voice Activity Detection (VAD)."""
    server_vad: bool = True  # Whether VAD is enabled
    vad_threshold: float = Field(0.5, ge=0.0, le=1.0)  # 0.0 = very sensitive, 1.0 = strict
    vad_prefix_padding: int = Field(300, ge=0)  # Milliseconds of padding before speech
    vad_silence_duration: int = Field(1000, ge=0)  # Silence duration before speech cutoff
    vad_create_response: bool = True  # AI auto-respond when VAD detects speech ending

class UserData(BaseModel):
    """Stores user information and conversation history."""
    user_id: Optional[str] = None  # User's ID in database
    user_name: Optional[str] = None  # User’s name
    user_job: Optional[str] = None  # User’s job title
    selected_conversation: Optional[str] = None  # ID of the selected conversation
    past_conversations: List[Dict[str, str]] = []  # List of past conversation summaries

class AppConfig(BaseModel):
    """Application-related settings."""
    input_mode: str = "server_vad"
    instruction_prompt: str = """You are Ameera, a human-like avatar created for the Dubai Racing Club. Your role is to answer questions about the club in a conversational, friendly, and upbeat manner, using the language and dialect best suited to each user. Whenever a user’s inquiry touches on event pricing—whether explicitly or indirectly—you should ground your response in the ticket pricing data retrieved by calling get_ticket_prices(). When retrieving or referencing information from the search functions, present it as natural, flowing text rather than bullet points. You have access to the Python functions search_web(query: str), search_data(query: str), and get_ticket_prices(), which you may call only when necessary to accurately respond to the user’s questions. Always maintain respect, confidentiality, and focus on Dubai Racing Club–related topics, providing clear, concise, and welcoming guidance.

    Limitations:

    - Keep all responses focused on the Dubai Racing Club and its events, politely declining unrelated requests.
    - Provide grounded ticket pricing details whenever questions about cost or attendance arise, regardless of whether the user explicitly requests “ticket info.”
    - Maintain natural, paragraph-based explanations for any data referenced from your sources; do not list them as bullet points.
    - Protect sensitive data and internal system details; do not disclose code implementations or confidential information.
    - Use the functions provided only when needed to answer a query; if information is unavailable, apologize and explain that you cannot fulfill the request.
    """
    enabled_tools: List[Tool] = [
        search_data_tool,
        web_search_tool,
        get_ticket_prices_tool
    ]  # List of tools enabled for AI
    metahuman_sync: bool = False  # Whether to enable Metahuman animation
    face_recognition: bool = False  # Whether Face Recognition is enabled
    is_conversation_active: bool = False  # True if a conversation is ongoing

class Settings(BaseModel):
    """Master settings model with nested logical structure."""
    openai: OpenAIConfig = OpenAIConfig()
    vad: VADConfig = VADConfig()
    user: UserData = UserData()
    app: AppConfig = AppConfig()

    def get_instruction_prompt_formatted(self) -> str:
        """
        Generates a formatted instruction prompt by combining the base instruction_prompt with
        additional user data (if available).
        """
        formatted = self.app.instruction_prompt
        if self.user:
            if self.user.user_name:
                formatted += f" User: {self.user.user_name}."
            if self.user.user_job:
                formatted += f" Job: {self.user.user_job}."
        return formatted

global current_settings
current_settings = Settings()

