package bob.colbaskin.dgtu_spring2025

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.Box
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.ui.Alignment
import androidx.compose.ui.platform.LocalContext
import bob.colbaskin.dgtu_spring2025.ui.theme.DGTUSPRING2025Theme
import bob.colbaskin.dgtu_spring2025.utils.Lottie
import kotlinx.coroutines.delay

@SuppressLint("CustomSplashScreen")
class SplashActivity: ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            DGTUSPRING2025Theme {
                SplashScreen()
            }
        }
    }
}

@Composable
fun SplashScreen() {
    val context = LocalContext.current

    LaunchedEffect(true) {
        delay(3_000)
        context.startActivity(Intent(context, MainActivity::class.java))
        (context as? Activity)?.finish()
    }

    Box(
        contentAlignment = Alignment.Center
    ) {
        Lottie(lottieJson = R.raw.splash_animation)
    }
}