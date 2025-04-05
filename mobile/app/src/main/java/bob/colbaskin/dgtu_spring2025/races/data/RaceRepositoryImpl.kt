package bob.colbaskin.dgtu_spring2025.races.data

import android.util.Log
import bob.colbaskin.dgtu_spring2025.BuildConfig
import bob.colbaskin.dgtu_spring2025.races.domain.RaceRepository
import bob.colbaskin.dgtu_spring2025.races.domain.models.Race
import bob.colbaskin.dgtu_spring2025.races.domain.models.Runner
import io.socket.client.IO
import io.socket.client.Socket
import io.socket.emitter.Emitter
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.callbackFlow
import org.json.JSONObject

class RaceRepositoryImpl : RaceRepository {
    override val socket: Socket by lazy {
        IO.socket(BuildConfig.SOCKET_URL).apply {
            connect()
        }
    }

    override fun observeRaces(): Flow<Race> = callbackFlow {
        val listener = Emitter.Listener { data ->
            try {
                val json = data[0] as JSONObject
                val race = parseRace(json)
                trySend(race)
            } catch (e: Exception) {
                Log.e("RaceRepo", "Error parsing race", e)
                close(e)
            }
        }

        socket.on("race_update", listener)

        awaitClose {
            socket.off("race_update", listener)
        }
    }

    override fun parseRace(json: JSONObject): Race {
        val raceId = json.getString("race_id")
        val totalRaces = json.optInt("total_races", 0)
        val runnersArray = json.getJSONArray("runners")

        val runners = mutableListOf<Runner>()
        for (i in 0 until runnersArray.length()) {
            val runnerObj = runnersArray.getJSONObject(i)
            runners.add(
                Runner(
                    id = runnerObj.getString("runner_id"),
                    progress = runnerObj.getDouble("current_progress").toFloat(),
                    icon = getRunnerIcon(runnerObj),
                    finished = runnerObj.getBoolean("finished")
                )
            )
        }

        return Race(raceId, runners, totalRaces)
    }

    private fun getRunnerIcon(runner: JSONObject): String {
        return when (runner.getString("runner_id")) {
            "1" -> "🔴"
            "2" -> "🔵"
            "3" -> "🟡"
            "4" -> "🟢"
            "5" -> "🟣"
            "6" -> "⚫"
            else -> "👤"
        }
    }

    override fun disconnect() {
        socket.disconnect()
    }
}