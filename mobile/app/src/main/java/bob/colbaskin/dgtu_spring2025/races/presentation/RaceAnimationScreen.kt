package bob.colbaskin.dgtu_spring2025.races.presentation

import android.annotation.SuppressLint
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import androidx.hilt.navigation.compose.hiltViewModel
import bob.colbaskin.dgtu_spring2025.R
import bob.colbaskin.dgtu_spring2025.races.domain.models.Runner
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme
import bob.colbaskin.dgtu_spring2025.utils.Lottie

@Composable
fun RaceAnimationScreen(viewModel: RacesViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState

    Box(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(16.dp),
            verticalArrangement = Arrangement.spacedBy(16.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            when (val state = uiState) {
                is RaceUiState.Loading -> LoadingView()
                is RaceUiState.Error -> ErrorView(state.message)
                is RaceUiState.Success -> RaceContent(state)
            }
        }
1
        RunnerParamsDialog(viewModel)
    }
}

@Composable
private fun RunnerParamsDialog(viewModel: RacesViewModel) {
    viewModel.selectedRunnerId?.let { runnerId ->
        AlertDialog(
            onDismissRequest = { viewModel.hideRunnerParams() },
            title = { Text("Параметры бегуна #$runnerId") },
            text = {
                Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = viewModel.reactionTime,
                        onValueChange = { viewModel.reactionTime = it },
                        label = { Text("Время реакции (сек)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        isError = viewModel.reactionTimeError != null
                    )
                    if (viewModel.reactionTimeError != null) {
                        Text(viewModel.reactionTimeError!!, color = Color.Red)
                    }

                    OutlinedTextField(
                        value = viewModel.acceleration,
                        onValueChange = { viewModel.acceleration = it },
                        label = { Text("Ускорение (м/с²)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        isError = viewModel.accelerationError != null
                    )
                    if (viewModel.accelerationError != null) {
                        Text(viewModel.accelerationError!!, color = Color.Red)
                    }

                    OutlinedTextField(
                        value = viewModel.maxSpeed,
                        onValueChange = { viewModel.maxSpeed = it },
                        label = { Text("Макс. скорость (м/с)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        isError = viewModel.maxSpeedError != null
                    )
                    if (viewModel.maxSpeedError != null) {
                        Text(viewModel.maxSpeedError!!, color = Color.Red)
                    }

                    OutlinedTextField(
                        value = viewModel.speedDecay,
                        onValueChange = { viewModel.speedDecay = it },
                        label = { Text("Спад скорости (м/с²)") },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        isError = viewModel.speedDecayError != null
                    )
                    if (viewModel.speedDecayError != null) {
                        Text(viewModel.speedDecayError!!, color = Color.Red)
                    }
                }
            },
            confirmButton = {
                Button(
                    onClick = { viewModel.submitParams() },
                    enabled = listOf(
                        viewModel.reactionTime,
                        viewModel.acceleration,
                        viewModel.maxSpeed,
                        viewModel.speedDecay
                    ).all {
                        it.isNotBlank() && viewModel.reactionTimeError == null
                        && viewModel.accelerationError == null
                        && viewModel.maxSpeedError == null
                        && viewModel.speedDecayError == null
                    }
                ) {
                    Text("Отправить")
                }
            },
            dismissButton = {
                TextButton(onClick = {
                    viewModel.hideRunnerParams()
                    viewModel.showRunnerParams()
                }) {
                    Text("Отмена")
                }
            }
        )
    }
}

@Composable
private fun RaceContent(state: RaceUiState.Success) {
    state.runners.forEach { runner ->
        RunnerTrack(runner)
    }
}

@SuppressLint("UnusedBoxWithConstraintsScope")
@Composable
private fun RunnerTrack(runner: Runner, viewModel: RacesViewModel = hiltViewModel()) {
    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .height(50.dp)
            .clickable { viewModel.selectRunner(runner) }
    ) {
        val density = LocalDensity.current
        val textWidth = with(density) { 32.sp.toDp() }
        val maxOffset = maxWidth - textWidth - 24.dp

        val offsetX by animateDpAsState(
            targetValue = maxOffset * (runner.progress / 100f),
            animationSpec = tween(durationMillis = 500, easing = LinearEasing)
        )

        Box(
            modifier = Modifier
                .fillMaxSize()
                .clip(RoundedCornerShape(24.dp))
                .background(Color(0xFF823E39))
                .border(1.dp, CustomTheme.colors.raceBorder, RoundedCornerShape(24.dp))
        )

        Text(
            text = runner.icon,
            modifier = Modifier
                .offset(x = offsetX)
                .align(Alignment.CenterStart)
                .zIndex(1f)
                .padding(start = 6.dp),
            fontSize = 32.sp
        )

        Text(
            text = "🏁",
            modifier = Modifier
                .align(Alignment.CenterEnd)
                .padding(end = 16.dp)
                .rotate(90f),
            fontSize = 32.sp
        )
    }
}

@Composable
private fun LoadingView() {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            verticalArrangement = Arrangement.Center,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Lottie(lottieJson = R.raw.loading_steps)
            Text(
                "Загрузка данных...",
                color = CustomTheme.colors.text
            )
        }
    }
}

@Composable
private fun ErrorView(message: String) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        contentAlignment = Alignment.Center
    ) {
        Text("Ошибка: $message", color = Color.Red)
    }
}

@Preview
@Composable
private fun RaceAnimationScreenPreview() {
    RaceAnimationScreen()
}
