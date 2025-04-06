package bob.colbaskin.dgtu_spring2025

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import bob.colbaskin.dgtu_spring2025.navigation.AppNavHost
import bob.colbaskin.dgtu_spring2025.ui.theme.DGTUSPRING2025Theme
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
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

