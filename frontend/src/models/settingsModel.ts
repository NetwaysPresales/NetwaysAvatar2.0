export interface IOpenAIConfig {
  model: string;
  voice: string;
  temperature: number;
  max_tokens: number;
  enable_streaming: boolean;
}

export interface IVADConfig {
  server_vad: boolean;
  vad_threshold: number;
  vad_prefix_padding: number;
  vad_silence_duration: number;
  vad_create_response: boolean;
}

export interface IUserData {
  user_id?: string;
  user_name?: string;
  user_job?: string;
  selected_conversation?: string;
  past_conversations: { [key: string]: string }[];
}

export interface IAppConfig {
  input_mode: string;
  instruction_prompt: string;
  enabled_tools: ITool[];
  metahuman_sync: boolean;
  face_recognition: boolean;
  is_conversation_active: boolean;
}

export interface ITool {
  type: string;
  name: string;
  description?: string;
  parameters?: Record<string, unknown>;
}

export interface ISettings {
  openai: IOpenAIConfig;
  vad: IVADConfig;
  user: IUserData;
  app: IAppConfig;
}

// Default settings
export const defaultSettings: ISettings = {
  openai: {
    model: "gpt-4o-realtime-preview",
    voice: "alloy",
    temperature: 0.8,
    max_tokens: 500,
    enable_streaming: true,
  },
  vad: {
    server_vad: true,
    vad_threshold: 0.5,
    vad_prefix_padding: 300,
    vad_silence_duration: 200,
    vad_create_response: true,
  },
  user: {
    user_id: "",
    user_name: "",
    user_job: "",
    selected_conversation: "",
    past_conversations: [],
  },
  app: {
    input_mode: "server_vad",
    instruction_prompt: "You are a helpful AI assistant.",
    enabled_tools: [],
    metahuman_sync: false,
    face_recognition: false,
    is_conversation_active: false,
  },
};
