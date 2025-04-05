package bob.colbaskin.dgtu_spring2025.history.presentation

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import bob.colbaskin.dgtu_spring2025.history.domain.models.RaceItem
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import androidx.compose.material3.TextButton
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.ui.window.Dialog
import bob.colbaskin.dgtu_spring2025.ui.theme.CustomTheme

@Composable
fun HistoryScreen() {
    val raceItems = listOf(
        RaceItem(1, "2025-04-05T10:00:00", "2025-04-05T12:00:00"),
        RaceItem(2, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(3, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(4, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(5, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(6, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(7, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(8, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(9, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(10, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(11, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(12, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(13, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(14, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(15, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(16, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
        RaceItem(17, "2025-04-06T09:30:00", "2025-04-06T11:30:00"),
    )
    val selectedItemCount = remember { mutableIntStateOf(5) }
    val itemCounts = listOf(5, 10, 15, 20)
    var showDialog by remember { mutableStateOf(false) }

    Column(modifier = Modifier.padding(16.dp)) {
        Text(
            "Выберите число элементов:",
            color = CustomTheme.colors.text
        )
        Button(
            onClick = { showDialog = true },
            modifier = Modifier.fillMaxWidth(),
            colors = ButtonDefaults.buttonColors(
                containerColor = CustomTheme.colors.defaultButton,
                contentColor = CustomTheme.colors.text
            )
        ) {
            Text(
                "Выбрано: ${selectedItemCount.intValue} элементов",
                color = CustomTheme.colors.text
            )
        }

        val currentItems = raceItems.take(selectedItemCount.intValue)

        HistoryContent(
            historyItems = currentItems,
            onLoadMore = { /* api call */ }
        )

        if (showDialog) {
            ItemCountDialog(
                itemCounts = itemCounts,
                selectedItemCount = selectedItemCount.intValue,
                onItemSelected = { count ->
                    selectedItemCount.intValue = count
                    showDialog = false
                }
            )
        }
    }
}

@Composable
fun ItemCountDialog(
    itemCounts: List<Int>,
    selectedItemCount: Int,
    onItemSelected: (Int) -> Unit
) {
    Dialog(onDismissRequest = { }) {
        Card(
            modifier = Modifier.padding(16.dp),
            colors = CardDefaults.cardColors(
                containerColor = CustomTheme.colors.cardColor,
                contentColor = CustomTheme.colors.text
            )
        ) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text(
                    "Выберите число элементов:",
                    color = CustomTheme.colors.text
                )
                Spacer(modifier = Modifier.height(16.dp))

                itemCounts.forEach { count ->
                    TextButton(
                        onClick = { onItemSelected(count) },
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Text(
                            "$count элементов",
                            color = CustomTheme.colors.text
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun HistoryContent(historyItems: List<RaceItem>, onLoadMore: () -> Unit) {
    val state = rememberLazyListState()
    val isListAtEnd = state.layoutInfo.visibleItemsInfo.lastOrNull()?.index == historyItems.size - 1

    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        state = state
    ) {
        items(historyItems) { raceItem ->
            RaceCard(raceItem = raceItem)
        }

        item {
            if (isListAtEnd) {
                Button(
                    onClick = { onLoadMore() },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = CustomTheme.colors.defaultButton,
                        contentColor = CustomTheme.colors.text
                    )
                ) {
                    Text(
                        "Загрузить больше",
                        color = CustomTheme.colors.text
                    )
                }
            }
        }
    }
}

@Composable
fun RaceCard(raceItem: RaceItem) {
    Card(
        modifier = Modifier.padding(bottom = 8.dp),
        colors = CardDefaults.cardColors(
            containerColor = CustomTheme.colors.cardColor,
            contentColor = CustomTheme.colors.text
        )
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = "Race ID: ${raceItem.id}",
                modifier = Modifier.padding(bottom = 8.dp),
                color = CustomTheme.colors.text
            )
            Text(
                text = "Start Time: ${formatTimestamp(raceItem.startTime)}",
                modifier = Modifier.padding(bottom = 8.dp),
                color = CustomTheme.colors.text
            )
            Text(
                text = "End Time: ${formatTimestamp(raceItem.endTime)}",
                modifier = Modifier.padding(bottom = 8.dp),
                color = CustomTheme.colors.text
            )
        }
    }
}

fun formatTimestamp(timestamp: String): String {
    return try {
        val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
        val dateTime = LocalDateTime.parse(timestamp, DateTimeFormatter.ISO_DATE_TIME)
        dateTime.format(formatter)
    } catch (e: Exception) {
        "Invalid Time: $e"
    }
}
