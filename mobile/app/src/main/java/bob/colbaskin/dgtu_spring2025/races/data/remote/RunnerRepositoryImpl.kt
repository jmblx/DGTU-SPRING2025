package bob.colbaskin.dgtu_spring2025.races.data.remote

import android.util.Log
import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerApiService
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

class RunnerRepositoryImpl @Inject constructor(
    val runnerApi: RunnerApiService
): RunnerRepository {
    private val _cachedParams = mutableMapOf<Int, RunnerParamsDTO>()
    private val paramsFlow = MutableStateFlow(_cachedParams)

    override suspend fun putRunnerParams(id: Int, request: RunnerParamsDTO) {
        runnerApi.putRunnerParams(id, request)
        _cachedParams[id] = request
        paramsFlow.value = _cachedParams
    }

    override suspend fun getRunnersParams(): List<RunnerParamsDTO> {
        return try {
            val params = runnerApi.getRunnersParams()
            Log.d("RunnerRepositoryImpl", "getRunnersParams: $params")
            _cachedParams.clear()
            params.forEach { _cachedParams[it.runnerId] = it }
            paramsFlow.value = _cachedParams
            params
        } catch (e: Exception) {
            emptyList()
        }
    }

    override fun observeParams() = paramsFlow.asStateFlow()
}