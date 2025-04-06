package bob.colbaskin.dgtu_spring2025.races.domain.remote

import bob.colbaskin.dgtu_spring2025.races.domain.models.Race
import io.socket.client.Socket
import kotlinx.coroutines.flow.Flow
import org.json.JSONObject

interface RaceRepository {
    val socket: Socket

    fun observeRaces(): Flow<Race>

    fun parseRace(json: JSONObject): Race

    fun disconnect()
}