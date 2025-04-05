package bob.colbaskin.dgtu_spring2025.races.presentation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.convertToProbabilityWithSymbols
import bob.colbaskin.dgtu_spring2025.probabilities.domain.models.probabilities
import bob.colbaskin.dgtu_spring2025.utils.PreviewBox
import com.breens.beetablescompose.BeeTablesCompose
import com.patrykandpatrick.vico.compose.cartesian.CartesianChartHost
import com.patrykandpatrick.vico.compose.cartesian.axis.rememberBottom
import com.patrykandpatrick.vico.compose.cartesian.axis.rememberStart
import com.patrykandpatrick.vico.compose.cartesian.layer.point
import com.patrykandpatrick.vico.compose.cartesian.layer.rememberLineCartesianLayer
import com.patrykandpatrick.vico.compose.cartesian.rememberCartesianChart
import com.patrykandpatrick.vico.compose.common.component.rememberShapeComponent
import com.patrykandpatrick.vico.compose.common.fill
import com.patrykandpatrick.vico.core.cartesian.axis.HorizontalAxis
import com.patrykandpatrick.vico.core.cartesian.axis.VerticalAxis
import com.patrykandpatrick.vico.core.cartesian.data.CartesianChartModelProducer
import com.patrykandpatrick.vico.core.cartesian.data.lineSeries
import com.patrykandpatrick.vico.core.cartesian.layer.LineCartesianLayer
import com.patrykandpatrick.vico.core.common.shape.CorneredShape
import kotlinx.coroutines.runBlocking

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
                JetpackComposeRaceChart()
            }
        }
    }
}

@Composable
private fun JetpackComposeRaceChart(
    modelProducer: CartesianChartModelProducer,
    modifier: Modifier = Modifier,
) {
    CartesianChartHost(
        chart = rememberCartesianChart(
            rememberLineCartesianLayer(
                lineProvider = LineCartesianLayer.LineProvider.series(
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFFF8312F))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFFF8312F)), CorneredShape.Pill))
                        )
                    ),
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFF0074BA))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFF0074BA)), CorneredShape.Pill))
                        )
                    ),
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFFFCD53F))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFFFCD53F)), CorneredShape.Pill))
                        )
                    ),
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFF00D26A))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFF00D26A)), CorneredShape.Pill))
                        )
                    ),
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFF8D65C5))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFF8D65C5)), CorneredShape.Pill))
                        )
                    ),
                    LineCartesianLayer.Line(
                        fill = LineCartesianLayer.LineFill.single(fill(Color(0xFF000000))),
                        stroke = LineCartesianLayer.LineStroke.Continuous(),
                        pointProvider = LineCartesianLayer.PointProvider.single(
                            LineCartesianLayer.point(rememberShapeComponent(fill(Color(0xFF000000)), CorneredShape.Pill))
                        )
                    )
                )
            ),
            startAxis = VerticalAxis.rememberStart(),
            bottomAxis = HorizontalAxis.rememberBottom(),
        ),
        modelProducer = modelProducer,
        modifier = modifier,
    )
}

@Composable
fun JetpackComposeRaceChart(modifier: Modifier = Modifier) {
    val modelProducer = remember { CartesianChartModelProducer() }
    LaunchedEffect(Unit) {
        modelProducer.runTransaction {
            lineSeries {
                series(1, 2, 5, 3, 6, 2, 5, 3, 4, 1)
                series(6, 5, 4, 6, 3, 5, 4, 6, 5, 6)
                series(4, 3, 6, 4, 2, 6, 3, 2, 3, 4)
                series(2, 4, 2, 5, 4, 4, 6, 5, 6, 5)
                series(5, 6, 1, 2, 5, 1, 2, 4, 1, 2)
                series(3, 1, 3, 1, 2, 3, 1, 1, 2, 3)
            }
        }
    }
    JetpackComposeRaceChart(modelProducer, modifier)
}

@Composable
@Preview
private fun Preview() {
    val modelProducer = remember { CartesianChartModelProducer() }
    runBlocking {
        modelProducer.runTransaction {
            lineSeries {
                series(1, 2, 5, 3, 6, 2, 5, 3, 4, 1)
                series(6, 5, 4, 6, 3, 5, 4, 6, 5, 6)
                series(4, 3, 6, 4, 2, 6, 3, 2, 3, 4)
                series(2, 4, 2, 5, 4, 4, 6, 5, 6, 5)
                series(5, 6, 1, 2, 5, 1, 2, 4, 1, 2)
                series(3, 1, 3, 1, 2, 3, 1, 1, 2, 3)
            }
        }
    }
    PreviewBox { JetpackComposeRaceChart(modelProducer) }
}