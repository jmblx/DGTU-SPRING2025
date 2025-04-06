package bob.colbaskin.dgtu_spring2025.races.domain.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class RunnerParamsDTO(
    @SerialName("runner_id") val runnerId: Int,
    @SerialName("reaction_time") var reactionTime: Double,
    var acceleration: Double,
    @SerialName("max_speed") var maxSpeed: Double,
    @SerialName("speed_decay") var speedDecay: Double
)