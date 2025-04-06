package bob.colbaskin.dgtu_spring2025.probabilities.data.remote

import android.util.Log
import bob.colbaskin.dgtu_spring2025.probabilities.domain.remote.TablesApiService
import bob.colbaskin.dgtu_spring2025.probabilities.domain.remote.TablesRepository
import javax.inject.Inject

class TablesRepositoryImpl @Inject constructor(
    private val chartsApi: TablesApiService
): TablesRepository {

    override suspend fun getAllCharts(): String {
        return try {
            chartsApi.getAllCharts()
        } catch (e: Exception) {
            Log.e("Error", e.toString())
        }.toString()
    }
}