package bob.colbaskin.dgtu_spring2025.probabilities.domain.models

data class Probability(
    val val1: Float,
    val val2: Float,
    val val3: Float,
    val val4: Float,
    val val5: Float
)

val probabilities = listOf(
    Probability(0.1f, 0.2f, 0.93f, 0.4f, 0.55f),
    Probability(0.12f, 0.25f, 0.3f, 0.54f, 0.5f),
    Probability(0.1f, 0.32f, 0.3f, 0.4f, 0.5f),
    Probability(0.1f, 0.2f, 0.35f, 0.4f, 0.5f),
    Probability(0.156f, 0.2f, 0.3f, 0.4f, 0.5f),
    Probability(0.1f, 0.2f, 0.3f, 0.4f, 0.5f),
)

data class ProbabilityWithSymbol(
    val symbol: String,
    val val1: Float,
    val val2: Float,
    val val3: Float,
    val val4: Float,
    val val5: Float
)

fun convertToProbabilityWithSymbols(probabilities: List<Probability>, symbols: List<String>): List<ProbabilityWithSymbol> {
    return probabilities.mapIndexed { index, probability ->
        ProbabilityWithSymbol(
            symbol = symbols.getOrElse(index) { "" },
            val1 = probability.val1,
            val2 = probability.val2,
            val3 = probability.val3,
            val4 = probability.val4,
            val5 = probability.val5
        )
    }
}
