package bob.colbaskin.dgtu_spring2025.races.presentation

import android.annotation.SuppressLint
import android.util.Log
import androidx.compose.animation.core.Animatable
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.VectorConverter
import androidx.compose.animation.core.animateDp
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.updateTransition
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.rotate
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.zIndex
import androidx.core.graphics.rotationMatrix
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme
import kotlinx.coroutines.launch

@Composable
fun RaceAnimationScreen() {
    RaceSimulation()
}

@SuppressLint("UnusedBoxWithConstraintsScope")
@Composable
fun RaceSimulation() {
    val icons = listOf("🔴", "🔵", "🟡", "🟢", "🟣", "⚫")
    var isAnimated by remember { mutableStateOf(false) }
    val iconTransition = updateTransition(targetState = isAnimated)
    var boxWidth by remember { mutableStateOf(0.dp) }
    val density = LocalDensity.current.density
    val textSizeInDp = (26 * density).dp
    val iconXOffset by iconTransition.animateDp(
        transitionSpec = { tween(easing = LinearEasing) }
    ) { isAnimatedState ->
        if (!isAnimatedState) 0.dp else boxWidth - textSizeInDp
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        repeat(6) { index ->
            BoxWithConstraints (
                modifier = Modifier
                    .fillMaxWidth()
                    .height(50.dp)
                    .clip(RoundedCornerShape(24.dp))
                    .background(Color(0xFF823E39))
                    .border(1.dp, CustomTheme.colors.raceBorder, RoundedCornerShape(24.dp))
            ) {
                Text(
                    icons[index],
                    modifier = Modifier
                        .align(Alignment.CenterStart)
                        .padding(horizontal = 16.dp)
                        .offset(x = iconXOffset)
                        .onGloballyPositioned { boxWidth = maxWidth }
                        .zIndex(1f),
                    fontSize = 32.sp
                )
                Text(
                    text = "🏁",
                    fontSize = 50.sp,
                    modifier = Modifier
                        .offset(x = boxWidth - textSizeInDp)
                        .rotate(90f)
                        .zIndex(0f),
                )
            }
        }
        Button(
            onClick = { isAnimated = !isAnimated },
            enabled = !isAnimated,
            colors = ButtonDefaults.buttonColors(
                containerColor = CustomTheme.colors.defaultButton,
                contentColor = CustomTheme.colors.text
            )
        ) {
            Text(
                "Начать симуляцию!",
                color = CustomTheme.colors.text
            )
        }
    }
}

@Preview
@Composable
fun RaceAnimationScreenPreview() {
    RaceAnimationScreen()
}
