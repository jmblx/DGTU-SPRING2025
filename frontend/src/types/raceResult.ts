export interface RaceResult {
    [runnerId: string]: number;
}

export interface RacesData {
    races: {
        [raceId: string]: RaceResult;
    };
}

export interface ProcessedRace {
    raceId: string;
    results: {
        runnerId: string;
        position: number;
    }[];
}