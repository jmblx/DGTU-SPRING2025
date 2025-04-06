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

    var selectedRunnerId by mutableStateOf<Int?>(null)
        private set

    var reactionTime by mutableStateOf("")
    var acceleration by mutableStateOf("")
    var maxSpeed by mutableStateOf("")
    var speedDecay by mutableStateOf("")

    var reactionTimeError by mutableStateOf<String?>(null)
    var accelerationError by mutableStateOf<String?>(null)
    var maxSpeedError by mutableStateOf<String?>(null)
    var speedDecayError by mutableStateOf<String?>(null)

    init {
        observeRaces()
    }

    fun showRunnerParams() {
        reactionTime = ""
        acceleration = ""
        maxSpeed = ""
        speedDecay = ""
        reactionTimeError = null
        accelerationError = null
        maxSpeedError = null
        speedDecayError = null
    }

    fun hideRunnerParams() {
        selectedRunnerId = null
    }

    fun submitParams() {
        val isValid = validateInputs()

        if (isValid) {
            selectedRunnerId?.let { id ->
                val params = RunnerParamsDTO(
                    reactionTime = reactionTime.toDoubleOrNull() ?: 0.0,
                    acceleration = acceleration.toDoubleOrNull() ?: 0.0,
                    maxSpeed = maxSpeed.toDoubleOrNull() ?: 0.0,
                    speedDecay = speedDecay.toDoubleOrNull() ?: 0.0
                )
                viewModelScope.launch {
                    try {
                        runnerRepository.putRunnerParams(id, params)
                        hideRunnerParams()
                    } catch (e: HttpException) {
                        Log.e("API_ERROR", "Ошибка HTTP: ${e.code()} - ${e.message()}")
                        Log.e("API_ERROR", "Тело ошибки: ${e.response()?.errorBody()?.string()}")
                        _uiState.value = RaceUiState.Error("Ошибка: ${e.code()} - ${e.message()}")
                    }
                }
            }
        }
    }

    private fun validateInputs(): Boolean {
        var isValid = true

        val reactionTimeValue = reactionTime.toDoubleOrNull()
        if (reactionTimeValue == null || reactionTimeValue !in 0.1..0.3) {
            reactionTimeError = "Время реакции должно быть между 0.1 и 0.3 сек."
            isValid = false
        } else {
            reactionTimeError = null
        }

        val accelerationValue = acceleration.toDoubleOrNull()
        if (accelerationValue == null || accelerationValue !in 2.0..10.0) {
            accelerationError = "Ускорение должно быть между 2 и 10 м/с²."
            isValid = false
        } else {
            accelerationError = null
        }

        val maxSpeedValue = maxSpeed.toDoubleOrNull()
        if (maxSpeedValue == null || maxSpeedValue !in 7.0..12.0) {
            maxSpeedError = "Макс. скорость должна быть между 7 и 12 м/с."
            isValid = false
        } else {
            maxSpeedError = null
        }

        val speedDecayValue = speedDecay.toDoubleOrNull()
        if (speedDecayValue == null || speedDecayValue !in 0.05..0.5) {
            speedDecayError = "Спад скорости должен быть между 0.05 и 0.5 м/с²."
            isValid = false
        } else {
            speedDecayError = null
        }

        return isValid
    }

    fun selectRunner(runner: Runner) {
        selectedRunnerId = runner.id.toIntOrNull()
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

sealed class RaceUiState {
    object Loading : RaceUiState()
    data class Error(val message: String) : RaceUiState()
    data class Success(
        val runners: List<Runner>,
        val totalRaces: Int
    ) : RaceUiState()
}