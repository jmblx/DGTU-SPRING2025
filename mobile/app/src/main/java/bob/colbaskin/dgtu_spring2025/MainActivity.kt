package bob.colbaskin.dgtu_spring2025

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.navigation.compose.composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.rememberNavController
import bob.colbaskin.dgtu_spring2025.navigation.BottomNavBar
import bob.colbaskin.dgtu_spring2025.navigation.Screens
import bob.colbaskin.dgtu_spring2025.ui.theme.DGTUSPRING2025Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            DGTUSPRING2025Theme {
                AppNavHost()
            }
        }
    }
}

@Composable
fun AppNavHost() {
    val navController = rememberNavController()
    Scaffold (
        bottomBar = { BottomNavBar(navController = navController) }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = Screens.Races.route,
            modifier = Modifier.padding(innerPadding)
        ) {
            composable(route = Screens.Races.route) {
                Box(contentAlignment = Alignment.Center) {
                    Text("Races")
                }
            }

            composable(route = Screens.Analytics.route) {
                Box(contentAlignment = Alignment.Center) {
                    Text("Analytics")
                }
            }

            composable(route = Screens.History.route) {
                Box(contentAlignment = Alignment.Center) {
                    Text("History")
                }
            }
        }
    }
}

