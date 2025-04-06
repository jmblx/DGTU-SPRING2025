package bob.colbaskin.dgtu_spring2025.probabilities.domain.remote

interface TablesRepository {
    suspend fun getAllCharts(): String
}

