from pydantic import BaseModel
from typing import Optional

class State(BaseModel):
    """Stores real-time state information about the current conversation session."""
    session_active: bool = False         # Whether a session is currently active
    response_active: bool = False        # Whether AI is currently generating a response
    speaking_vad: bool = False           # Whether the AI detected user speech (Server VAD mode)
    speaking_ptt: bool = False           # Whether user audio is being streamed (for PTT & Server VAD)
    waiting_for_commit: bool = False     # True when waiting for commit in PTT mode
    last_event: Optional[str] = None     # Last received OpenAI event for tracking/debugging
    session_id: Optional[str] = None     # The ID of the current session (if provided)
    conversation_id: Optional[str] = None  # The ID of the current conversation (if applicable)

# Initialize conversation state globally
global current_state
current_state = State()

