export interface IState {
    session_active: boolean;
    response_active: boolean;
    speaking_vad: boolean;
    speaking_ptt: boolean;
    waiting_for_commit: boolean;
    last_event?: string;
    session_id?: string;
    conversation_id?: string;
};

// default state
export const defaultState: IState = {
    session_active: false,
    response_active: false,
    speaking_vad: false,
    speaking_ptt: false,
    waiting_for_commit: false,
    last_event: "",
    session_id: "",
    conversation_id: "",
};