package bob.colbaskin.dgtu_spring2025

import android.app.Application
import bob.colbaskin.dgtu_spring2025.races.data.workmanager.RunnerSyncWorker
import dagger.hilt.android.HiltAndroidApp

@HiltAndroidApp
class Application: Application() {
    override fun onCreate() {
        super.onCreate()
        RunnerSyncWorker.start(applicationContext)
    }
}