package bob.colbaskin.dgtu_spring2025.navigation

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.DirectionsRun
import androidx.compose.material.icons.filled.BarChart
import androidx.compose.material.icons.filled.History
import androidx.compose.ui.graphics.vector.ImageVector

sealed class Screens (
    val route: String,
    val label: String,
    val icon: ImageVector
) {
    data object Races: Screens("races", "Забеги", Icons.AutoMirrored.Filled.DirectionsRun)
    data object Analytics: Screens("analytics", "Аналитика", Icons.Default.BarChart)
    data object History: Screens("history", "История", Icons.Default.History)
}