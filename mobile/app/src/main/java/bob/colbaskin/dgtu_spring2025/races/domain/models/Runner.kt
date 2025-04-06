package bob.colbaskin.dgtu_spring2025.races.domain.models

data class Runner(
    val id: String,
    val progress: Float,
    val icon: String,
    val finished: Boolean
)
