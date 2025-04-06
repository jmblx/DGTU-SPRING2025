export interface PositionProbabilities {
    [runnerId: string]: {
        position_1: number;
        position_2: number;
        position_3: number;
        position_4: number;
        position_5: number;
        position_6: number;
    };
}

export interface TopProbabilities {
    [runnerId: string]: number;
}

export interface PairProbabilities {
    [runnerId: string]: {
        [opponentId: string]: number | null;
    };
}

export interface ProbabilitiesPairResponse {
    pair_matrix: PairProbabilities;
}

export interface ProbabilitiesResponse {
    position_probabilities: PositionProbabilities;
}

export interface ProbabilitiesTopResponse {
    top2_probabilities: TopProbabilities;
    top3_probabilities: TopProbabilities;
}