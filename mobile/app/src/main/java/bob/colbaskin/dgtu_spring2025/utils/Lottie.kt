package bob.colbaskin.dgtu_spring2025.utils

import androidx.annotation.RawRes
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import com.airbnb.lottie.compose.LottieAnimation
import com.airbnb.lottie.compose.LottieCompositionSpec
import com.airbnb.lottie.compose.LottieConstants
import com.airbnb.lottie.compose.animateLottieCompositionAsState
import com.airbnb.lottie.compose.rememberLottieComposition

@Composable
fun Lottie(
    @RawRes lottieJson: Int,
    modifier: Modifier = Modifier,
) {

    val composition by rememberLottieComposition(
        LottieCompositionSpec.RawRes(lottieJson)
    )

    val compositionProgress by animateLottieCompositionAsState(
        composition = composition,
        iterations = LottieConstants.IterateForever,
        isPlaying = true
    )

    LottieAnimation(
        modifier = modifier,
        composition = composition,
        progress = { compositionProgress }
    )
}