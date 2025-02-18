export interface OpenAIConfig {
  model: string;
  voice: string;
  temperature: number;
  maxTokens: number;
  enableStreaming: boolean;
}

export interface VADConfig {
  serverVAD: boolean;
  vadThreshold: number;
  vadPrefixPadding: number;
  vadSilenceDuration: number;
  vadCreateResponse: boolean;
}

export interface UserData {
  user_id?: string;
  user_name?: string;
  user_job?: string;
  selected_conversation?: string | null;
  past_conversations: { id: string; title: string }[];
}

export interface AppConfig {
  input_mode: string; // "server_vad" or "ptt"
  instruction_prompt: string;
  enabled_tools: string[];
  metahuman_sync: boolean;
  face_recognition: boolean;
  is_conversation_active: boolean;
}

export interface Settings {
  openai: OpenAIConfig;
  vad: VADConfig;
  user: UserData;
  app: AppConfig;
}

export const defaultSettings: Settings = {
  openai: {
    model: "gpt-4o-realtime-preview",
    voice: "alloy",
    temperature: 0.8,
    maxTokens: 500,
    enableStreaming: true,
  },
  vad: {
    serverVAD: true,
    vadThreshold: 0.5,
    vadPrefixPadding: 300,
    vadSilenceDuration: 200,
    vadCreateResponse: true,
  },
  user: {
    user_id: undefined,
    user_name: "",
    user_job: "",
    selected_conversation: null,
    past_conversations: [],
  },
  app: {
    input_mode: "server_vad", // "server_vad" or "ptt"
    instruction_prompt: "You are a helpful AI assistant.",
    enabled_tools: ["search"],
    metahuman_sync: false,
    face_recognition: false,
    is_conversation_active: false,
  },
};
