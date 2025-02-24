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
            "type": type,
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }

search_data_tool = Tool(
    type="function",
    name="search_data",
    description="Reads content from Dubai_Racin_Club.md and returns it as text.",
    parameters=None  # No input parameters required
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
    vad_silence_duration: int = Field(200, ge=0)  # Silence duration before speech cutoff
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
    instruction_prompt: str = "You are Ameera, a helpful AI assistant that works for Dubai Racing Club. Respond in a friendly and conversational manner, in the language of the user."
    enabled_tools: List[Tool] = [
        search_data_tool
    ]  # List of tools enabled for AI (e.g., retrieval, code_interpreter)
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

