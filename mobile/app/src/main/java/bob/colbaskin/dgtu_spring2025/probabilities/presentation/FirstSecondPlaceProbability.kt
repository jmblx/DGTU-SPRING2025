package bob.colbaskin.dgtu_spring2025.probabilities.presentation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.style.TextAlign
import androidx.hilt.navigation.compose.hiltViewModel
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.probabilities
import bob.colbaskin.dgtu_spring2025.races.presentation.RacesViewModel
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme

import com.breens.beetablescompose.BeeTablesCompose

@Composable
fun FirstSecondPlaceProbability (viewModel: RacesViewModel = hiltViewModel()) {
    val titles = listOf("🔴", "🔵", "🟡", "🟢", "🟣", "⚫")
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        BeeTablesCompose(
            data = probabilities,
            enableTableHeaderTitles = true,
            disableVerticalDividers = true,
            headerTableTitles = titles,
            headerTitlesBackGroundColor = CustomTheme.colors.headerTable,
            tableRowColors = listOf(
                CustomTheme.colors.tableRow,
                CustomTheme.colors.tableRow,
            ),
            contentAlignment= Alignment.Center,
            textAlign = TextAlign.Center,
            headerTitlesTextStyle = TextStyle(color = Color.White)
        )
    }
}