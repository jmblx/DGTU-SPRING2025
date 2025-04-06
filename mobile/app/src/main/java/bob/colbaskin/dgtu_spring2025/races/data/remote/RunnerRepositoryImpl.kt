package bob.colbaskin.dgtu_spring2025.races.data.remote

import android.util.Log
import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerApiService
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import javax.inject.Inject

class RunnerRepositoryImpl @Inject constructor(
    val runnerApi: RunnerApiService
): RunnerRepository {

    override suspend fun putRunnerParams(id: Int, request: RunnerParamsDTO) {
        try {
            runnerApi.putRunnerParams(id, request)
        } catch (e: Exception) {
            Log.e("Error", "putRunnerParams: ${e.message}")
        }
    }

    override suspend fun getRunnersParams(): List<RunnerParamsDTO> {
            val params = runnerApi.getRunnersParams()
            Log.d("RunnerRepositoryImpl", "getRunnersParams: $params")
            return params
    }

    override suspend fun getRacesStatsLast(): String{
        return try {
            runnerApi.getRacesStatsLast().trim()
        } catch (e: Exception) {
            Log.e("Error", "getRacesStatsLast: ${e.message}")
        }.toString()

    }
}