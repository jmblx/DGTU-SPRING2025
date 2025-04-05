package bob.colbaskin.dgtu_spring2025.probabilities.presentation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.convertToProbabilityWithSymbols
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.probabilities
import com.breens.beetablescompose.BeeTablesCompose


@Composable
fun PlacementProbabilities() {
    val titles = listOf("1", "2", "3", "4", "5", "6")
    val symbols = listOf("🔴", "🔵", "🟡", "🟢", "🟣", "⚫")
    Box(
        modifier = Modifier
            .fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        BeeTablesCompose(
            data = convertToProbabilityWithSymbols(probabilities, symbols),
            enableTableHeaderTitles = true,
            disableVerticalDividers = true,
            headerTableTitles = titles,
            headerTitlesBackGroundColor = Color.DarkGray,
            tableRowColors = listOf(
                Color.LightGray,
                Color.LightGray,
            ),
            contentAlignment= Alignment.Center,
            textAlign = TextAlign.Center
        )
    }
}