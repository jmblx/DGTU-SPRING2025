package bob.colbaskin.dgtu_spring2025.races.data.remote

import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerApiService
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import javax.inject.Inject

class RunnerRepositoryImpl @Inject constructor(
    val runnerApi: RunnerApiService
): RunnerRepository {

    override suspend fun putRunnerParams(id: Int, request: RunnerParamsDTO) {
        runnerApi.putRunnerParams(id, request)
    }
}