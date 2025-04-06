package bob.colbaskin.dgtu_spring2025.races.domain.remote

import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO
import retrofit2.http.Body
import retrofit2.http.PUT
import retrofit2.http.Path

interface RunnerApiService {

    @PUT("v1/runners/{runner_id}")
    suspend fun putRunnerParams(
        @Path("runner_id") runnerId: Int,
        @Body runnerParamsDTO: RunnerParamsDTO
    )
}