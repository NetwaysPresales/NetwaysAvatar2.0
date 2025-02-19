import { ISettings } from "./settingsModel";
import { IState } from "./stateModel";

export interface DataSyncPayload {
    settings?: ISettings;
    state?: IState;
}