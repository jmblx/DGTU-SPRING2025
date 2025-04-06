package bob.colbaskin.dgtu_spring2025.races.domain.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class RunnerParamsDTO(
    @SerialName("reaction_time") val reactionTime: Double,
    val acceleration: Double,
    @SerialName("max_speed") val maxSpeed: Double,
    @SerialName("speed_decay") val speedDecay: Double
)