from pydantic import BaseModel, Field
from typing import Dict, List, Optional

class OpenAIConfig(BaseModel):
    """Settings related to OpenAI model behavior and processing."""
    model: str = "gpt-4o-realtime-preview"
    voice: str = "alloy"
    temperature: float = Field(0.8, ge=0.0, le=1.0)  # AI creativity level (0-1)
    max_tokens: int = Field(500, gt=0)  # Maximum tokens per response
    enable_streaming: bool = True  # Whether responses are streamed

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
    instruction_prompt: str = "You are a helpful AI assistant."
    enabled_tools: List[str] = []  # List of tools enabled for AI (e.g., "retrieval", "code_interpreter")
    metahuman_sync: bool = False  # Whether to enable Metahuman animation
    face_recognition: bool = False  # Whether Face Recognition is enabled
    is_conversation_active: bool = False  # True if a conversation is ongoing

class Settings(BaseModel):
    """Master settings model with nested logical structure."""
    openai: OpenAIConfig = OpenAIConfig()
    vad: VADConfig = VADConfig()
    user: UserData = UserData()
    app: AppConfig = AppConfig()


