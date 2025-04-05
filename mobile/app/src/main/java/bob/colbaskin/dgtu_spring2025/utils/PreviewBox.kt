package bob.colbaskin.dgtu_spring2025.utils

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.padding
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

@Composable
fun PreviewBox(content: @Composable BoxScope.() -> Unit) {
    Box(modifier = Modifier.background(Color.White).padding(16.dp), content = content)
}