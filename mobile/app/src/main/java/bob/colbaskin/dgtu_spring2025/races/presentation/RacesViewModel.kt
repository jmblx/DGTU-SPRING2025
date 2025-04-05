package bob.colbaskin.dgtu_spring2025.races.presentation

import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import bob.colbaskin.dgtu_spring2025.races.domain.RaceRepository
import bob.colbaskin.dgtu_spring2025.races.domain.models.Runner
import dagger.hilt.android.lifecycle.HiltViewModel
import javax.inject.Inject
import androidx.compose.runtime.State
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.launchIn
import kotlinx.coroutines.flow.onEach

sealed class RaceUiState {
    object Loading : RaceUiState()
    data class Error(val message: String) : RaceUiState()
    data class Success(
        val runners: List<Runner>,
        val totalRaces: Int
    ) : RaceUiState()
    data class Waiting(val totalRaces: Int) : RaceUiState()
}

@HiltViewModel
class RacesViewModel @Inject constructor(
    private val repository: RaceRepository
) : ViewModel() {

    private val _uiState = mutableStateOf<RaceUiState>(RaceUiState.Loading)
    val uiState: State<RaceUiState> = _uiState

    init {
        observeRaces()
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