package bob.colbaskin.dgtu_spring2025.probabilities.domain.remote

import retrofit2.http.GET

interface TablesApiService {

    @GET("v1/probabilities")
    suspend fun getAllCharts(): String
}