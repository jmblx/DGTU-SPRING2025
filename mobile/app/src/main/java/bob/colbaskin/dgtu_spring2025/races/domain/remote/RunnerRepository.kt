package bob.colbaskin.dgtu_spring2025.races.domain.remote

import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO


interface RunnerRepository {

    suspend fun putRunnerParams(runnerId: Int, request: RunnerParamsDTO)

    suspend fun getRunnersParams(): List<RunnerParamsDTO>

}