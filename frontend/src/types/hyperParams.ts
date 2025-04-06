export interface IHyperParams {
    runner_id: number,
    reaction_time: number,
    acceleration: number,
    max_speed: number,
    speed_decay: number,
}

export interface UpdateParams {
    reaction_time?: number;
    acceleration?: number;
    max_speed?: number;
    speed_decay?: number;
}