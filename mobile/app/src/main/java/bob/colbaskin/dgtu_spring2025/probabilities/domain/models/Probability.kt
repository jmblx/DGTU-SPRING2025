package bob.colbaskin.dgtu_spring2025.probabilities.domain.models

data class Probability(
    val val1: Int,
    val val2: Int,
    val val3: Int,
    val val4: Int,
    val val5: Int,
    val val6: Int
)

val probabilities = listOf(
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
    Probability(1, 1, 1, 1, 1, 1),
)

data class ProbabilityWithSymbol(
    val symbol: String,
    val val1: Int,
    val val2: Int,
    val val3: Int,
    val val4: Int,
    val val5: Int
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

data class Response(
    val title: List<String>,
    val probability: List<Probability>
)
