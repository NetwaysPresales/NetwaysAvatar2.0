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
  userName: string;
  userJob: string;
  selectedConversation: string | null;
  pastConversations: { id: string; title: string }[];
}

export interface AppConfig {
  instructionPrompt: string;
  enabledTools: string[];
  metahumanSync: boolean;
  faceRecognition: boolean;
  isConversationActive: boolean;
}

export interface Settings {
  openai: OpenAIConfig;
  vad: VADConfig;
  user: UserData;
  app: AppConfig;
}

// ✅ Default settings (mirroring backend defaults)
export let defaultSettings: Settings = {
  openai: {
    model: "gpt-4o-realtime-preview",
    voice: "alloy",
    temperature: 0.7,
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
    userName: "",
    userJob: "",
    selectedConversation: null,
    pastConversations: [],
  },
  app: {
    instructionPrompt: "You are a helpful AI assistant.",
    enabledTools: ["search"],
    metahumanSync: false,
    faceRecognition: false,
    isConversationActive: false,
  },
};

// ✅ Function to update settings dynamically
export const updateSettings = <K extends keyof Settings>(
  key: K,
  value: Settings[K]
) => {
  defaultSettings = { ...defaultSettings, [key]: value };
  console.log(`Updated setting: ${key} →`, value);
};

// ✅ Function to retrieve the current settings
export const getSettings = (): Settings => {
  return defaultSettings;
};
