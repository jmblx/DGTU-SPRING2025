package bob.colbaskin.dgtu_spring2025.ui.theme

import androidx.compose.runtime.Immutable
import androidx.compose.runtime.staticCompositionLocalOf
import androidx.compose.ui.graphics.Color

@Immutable
data class CustomColors(
    val background: Color,
    val activeButton: Color,
    val defaultButton: Color,
    val raceBorder: Color,
    val bottomBar: Color,
    val headerTable: Color,
    val tableRow: Color,
    val cardColor: Color,
    val text: Color
)

val localCustomColors = staticCompositionLocalOf {
    CustomColors(
        background = Color.Unspecified,
        activeButton = Color.Unspecified,
        defaultButton = Color.Unspecified,
        raceBorder = Color.Unspecified,
        bottomBar = Color.Unspecified,
        headerTable = Color.Unspecified,
        tableRow = Color.Unspecified,
        cardColor = Color.Unspecified,
        text = Color.Unspecified
    )
}

val customColorsDark = CustomColors(
    background = Color(0xFF1C1C1C),
    activeButton = Color(0xFF3AC7FF),
    defaultButton = Color(0xFF2F2F2F),
    raceBorder = Color(0xFFFFFFFF),
    bottomBar = Color(0xFF303030),
    headerTable = Color.DarkGray,
    tableRow = Color.LightGray,
    cardColor = Color(0xFF323131),
    text = Color(0xFFFFFFFF)
)
val customColorsLight = CustomColors(
    background = Color(0xFFF1F1F1),
    activeButton = Color(0xFF1E88E5),
    defaultButton = Color(0xFFBDBDBD),
    raceBorder = Color(0xFF000000),
    bottomBar = Color(0xFFD2D2D2),
    headerTable = Color.DarkGray,
    tableRow = Color.LightGray,
    cardColor = Color(0xFFD8D8D8),
    text = Color(0xFF000000)
)
