package bob.colbaskin.dgtu_spring2025.races.presentation

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import bob.colbaskin.dgtu_spring2025.utils.TabItem
import bob.colbaskin.dgtu_spring2025.utils.TabScreen

@Composable
fun RacesScreen() {
    val tabs = listOf(
        TabItem(0, "Анимация забега"),
        TabItem(1, "Статистика забега")
    )

    TabScreen(
        tabs = tabs
    ) { selectedTabIndex ->
        when (selectedTabIndex) {
            0 -> RaceAnimationScreen()
            1 -> RaceAnalyticsScreen()
            else -> Text("Неизвестная вкладка")
        }
    }
}