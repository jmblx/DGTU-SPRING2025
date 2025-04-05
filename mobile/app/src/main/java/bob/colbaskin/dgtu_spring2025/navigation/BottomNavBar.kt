package bob.colbaskin.dgtu_spring2025.navigation

import androidx.compose.foundation.layout.RowScope
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.navigation.NavDestination
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavHostController
import androidx.navigation.compose.currentBackStackEntryAsState
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme

@Composable
fun BottomNavBar(navController: NavHostController) {
    val screens = listOf(
        Screens.Races,
        Screens.Analytics,
        Screens.History
    )

    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    val bottomBarDestination = screens.any { it.route ==  currentDestination?.route }
    if (bottomBarDestination) {
        NavigationBar(
            containerColor = CustomTheme.colors.bottomBar,
            contentColor = CustomTheme.colors.text
        ) {
            screens.forEach { screen ->
                AddItem (
                    screen,
                    currentDestination,
                    navController
                )
            }
        }
    }
}

@Composable
fun RowScope.AddItem(
    screen: Screens,
    currentDestination: NavDestination?,
    navController: NavHostController,
) {
    val isSelected = currentDestination?.hierarchy?.any {
        it.route == screen.route
    } == true
    NavigationBarItem(
        selected = isSelected,
        onClick = {
            navController.navigate(screen.route) {
                popUpTo(navController.graph.findStartDestination().id)
                launchSingleTop = true
            }
        },
        icon = {
            Icon(
                imageVector = screen.icon,
                contentDescription = null,
                tint = CustomTheme.colors.text
            )
        },
        label = {
            Text(
                screen.label,
                color = CustomTheme.colors.text
            )
        }
    )
}
