package bob.colbaskin.dgtu_spring2025.navigation

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import bob.colbaskin.dgtu_spring2025.history.presentation.HistoryScreen
import bob.colbaskin.dgtu_spring2025.probabilities.presentation.ProbabilitiesScreen
import bob.colbaskin.dgtu_spring2025.races.presentation.RacesScreen
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme
import com.google.accompanist.systemuicontroller.rememberSystemUiController

@Composable
fun AppNavHost() {
    val navController = rememberNavController()
    Scaffold (
        bottomBar = { BottomNavBar(navController = navController) }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screens.Races.route,
            modifier = Modifier
                .padding(innerPadding)
                .background(CustomTheme.colors.background)
        ) {
            composable(route = Screens.Races.route) {
                Box(contentAlignment = Alignment.Center) {
                    RacesScreen()
                }
            }

            composable(route = Screens.Analytics.route) {
                Box(contentAlignment = Alignment.Center) {
                    ProbabilitiesScreen()
                }
            }

            composable(route = Screens.History.route) {
                Box(contentAlignment = Alignment.Center) {
                    HistoryScreen()
                }
            }
        }
    }
}