package bob.colbaskin.dgtu_spring2025.probabilities.presentation

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import bob.colbaskin.dgtu_spring2025.utils.TabItem
import bob.colbaskin.dgtu_spring2025.utils.TabScreen

@Composable
fun ProbabilitiesScreen() {
    val tabs = listOf(
        TabItem(0, "Вероятности по местам"),
        TabItem(1, "Топ 2/3"),
        TabItem(2, "1-е и 2-е места")
    )

    TabScreen(
        tabs = tabs
    ) { selectedTabIndex ->
        when (selectedTabIndex) {
            0 -> PlacementProbabilities()
            1 -> Top2or3Probability()
            2 -> FirstSecondPlaceProbability()
            else -> Text("Неизвестная вкладка")
        }
    }
}