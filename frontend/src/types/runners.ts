export interface Runner {
    runner_id: number;
    current_progress: number;
    time: number;
    finished: boolean;
}

export interface RaceUpdateData {
    race_id: string;
    runners: Runner[];
    stream_complete?: boolean;
    stream_duration?: number;
    next_stream_in?: number;
}
