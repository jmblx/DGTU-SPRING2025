package bob.colbaskin.dgtu_spring2025.races.presentation

import android.util.Log
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RaceRepository
import bob.colbaskin.dgtu_spring2025.races.domain.models.Runner
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import androidx.compose.runtime.State
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import bob.colbaskin.dgtu_spring2025.races.domain.models.RunnerParamsDTO
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach
import kotlinx.coroutines.launch
import retrofit2.HttpException

@HiltViewModel
class RacesViewModel @Inject constructor(
    private val repository: RaceRepository,
    private val runnerRepository: RunnerRepository
) : ViewModel() {

    private val _uiState = mutableStateOf<RaceUiState>(RaceUiState.Loading)
    val uiState: State<RaceUiState> = _uiState

    private val _runnerParamsState = mutableStateOf<RunnerParamsState?>(null)
    val runnerParamsState: State<RunnerParamsState?> = _runnerParamsState

    private var cachedParams by mutableStateOf<Map<Int, RunnerParamsDTO>>(emptyMap())

    init {
        observeRaces()
        observeRunnerParams()
        viewModelScope.launch {
            Log.d("RacesViewModel", "${runnerRepository.getRunnersParams()}")
        }
    }

    private fun observeRunnerParams() {
        runnerRepository.observeParams()
            .onEach { params ->
                cachedParams = params
                updateCurrentParamsState()
            }
            .launchIn(viewModelScope)
    }

    private fun updateCurrentParamsState() {
        _runnerParamsState.value?.let { currentState ->
            cachedParams[currentState.runnerId]?.let { newParams ->
                _runnerParamsState.value = currentState.copy(
                    params = newParams,
                    errors = validateParams(newParams)
                )
            }
        }
    }

    fun selectRunner(runner: Runner) {
        val runnerId = runner.id.toIntOrNull() ?: return
        val params = cachedParams[runnerId] ?: RunnerParamsDTO(
            runnerId = runnerId,
            reactionTime = 0.0,
            acceleration = 0.0,
            maxSpeed = 0.0,
            speedDecay = 0.0
        )

        _runnerParamsState.value = RunnerParamsState(
            runnerId = runnerId,
            params = params,
            errors = validateParams(params)
        )
    }

    fun updateParam(field: RunnerParamField, value: String) {
        val currentState = _runnerParamsState.value ?: return
        val newParams = currentState.params.copy().apply {
            when(field) {
                RunnerParamField.REACTION_TIME -> reactionTime = value.toDoubleOrNull() ?: 0.0
                RunnerParamField.ACCELERATION -> acceleration = value.toDoubleOrNull() ?: 0.0
                RunnerParamField.MAX_SPEED -> maxSpeed = value.toDoubleOrNull() ?: 0.0
                RunnerParamField.SPEED_DECAY -> speedDecay = value.toDoubleOrNull() ?: 0.0
            }
        }

        _runnerParamsState.value = currentState.copy(
            params = newParams,
            errors = validateParams(newParams)
        )
    }

    private fun validateParams(params: RunnerParamsDTO): Map<RunnerParamField, String> {
        val errors = mutableMapOf<RunnerParamField, String>()

        if (params.reactionTime !in 0.1..0.3) {
            errors[RunnerParamField.REACTION_TIME] = "Должно быть между 0.1 и 0.3 сек"
        }
        if (params.acceleration !in 2.0..10.0) {
            errors[RunnerParamField.ACCELERATION] = "Должно быть между 2 и 10 м/с²"
        }
        if (params.maxSpeed !in 7.0..12.0) {
            errors[RunnerParamField.MAX_SPEED] = "Должно быть между 7 и 12 м/с"
        }
        if (params.speedDecay !in 0.05..0.5) {
            errors[RunnerParamField.SPEED_DECAY] = "Должно быть между 0.05 и 0.5 м/с²"
        }

        return errors
    }

    fun submitParams() {
        val currentState = _runnerParamsState.value ?: return
        if (currentState.errors.isNotEmpty()) return

        viewModelScope.launch {
            try {
                runnerRepository.putRunnerParams(currentState.runnerId, currentState.params)
                _runnerParamsState.value = null
            } catch (e: HttpException) {
                _runnerParamsState.value = currentState.copy(
                    error = "Ошибка сохранения: ${e.code()} - ${e.message()}"
                )
                Log.e("API_ERROR", "Ошибка HTTP", e)
            }
        }
    }

    fun hideRunnerParams() {
        _runnerParamsState.value = null
    }

    private fun observeRaces() {
        repository.observeRaces()
            .onEach { race ->
                _uiState.value = RaceUiState.Success(
                    runners = race.runners,
                    totalRaces = race.totalRaces
                )
            }
            .catch { e ->
                _uiState.value = RaceUiState.Error(
                    message = "Ошибка подключения: ${e.message ?: "Неизвестная ошибка"}"
                )
            }
            .launchIn(viewModelScope)
    }
}

data class RunnerParamsState(
    val runnerId: Int,
    val params: RunnerParamsDTO,
    val errors: Map<RunnerParamField, String>,
    val error: String? = null
) {
    fun isValid() = errors.isEmpty()
}

enum class RunnerParamField {
    REACTION_TIME, ACCELERATION, MAX_SPEED, SPEED_DECAY
}

sealed class RaceUiState {
    object Loading : RaceUiState()
    data class Error(val message: String) : RaceUiState()
    data class Success(
        val runners: List<Runner>,
        val totalRaces: Int
    ) : RaceUiState()
}