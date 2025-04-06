package bob.colbaskin.dgtu_spring2025.races.domain.models

data class Race(
    val id: String,
    val runners: List<Runner>,
    val totalRaces: Int
)
