package bob.colbaskin.dgtu_spring2025.races.presentation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.convertToProbabilityWithSymbols
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.probabilities
import com.breens.beetablescompose.BeeTablesCompose

@Composable
fun RaceAnalyticsScreen() {
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        val titles = listOf("🔴", "🔵", "🟡", "🟢", "🟣", "⚫")
        val symbols = listOf("1", "2", "3", "4")
        item {
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
                contentAlignment = Alignment.Center,
                textAlign = TextAlign.Center
            )
        }
        item {
            Box(
                modifier = Modifier.fillMaxSize(),
                contentAlignment = Alignment.Center
            ) {
                Text(text = "тут будет график", color = Color.Green)
            }
        }
    }
}