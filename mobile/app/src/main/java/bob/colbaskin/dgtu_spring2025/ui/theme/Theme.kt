package bob.colbaskin.dgtu_spring2025.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider

@Composable
fun DGTUSPRING2025Theme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    // Dynamic color is available on Android 12+
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val customColors = if (darkTheme) customColorsDark else customColorsLight


    CompositionLocalProvider (
        localCustomColors provides customColors,
        content = content
    )
}

object CustomTheme {
    val colors: CustomColors
        @Composable get() = localCustomColors.current
}