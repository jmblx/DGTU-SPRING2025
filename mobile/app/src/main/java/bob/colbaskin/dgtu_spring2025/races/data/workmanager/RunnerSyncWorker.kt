package bob.colbaskin.dgtu_spring2025.races.data.workmanager

import android.content.Context
import android.util.Log
import androidx.work.CoroutineWorker
import androidx.work.ExistingWorkPolicy
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.WorkerParameters
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import java.util.concurrent.TimeUnit
import javax.inject.Inject

class RunnerSyncWorker(
    context: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(context, workerParams) {

    @Inject
    lateinit var repository: RunnerRepository

    override suspend fun doWork(): Result {
        Log.d("RunnerSyncWorker", "doWork")
        return try {
            repository.getRunnersParams()
            scheduleNext()
            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }

    private fun scheduleNext() {
        val workRequest = OneTimeWorkRequestBuilder<RunnerSyncWorker>()
            .setInitialDelay(25, TimeUnit.SECONDS)
            .build()

        WorkManager.getInstance(applicationContext)
            .enqueueUniqueWork("UNIQUE_RUNNER_SYNC", ExistingWorkPolicy.REPLACE, workRequest)
    }

    companion object {
        fun start(context: Context) {
            val workRequest = OneTimeWorkRequestBuilder<RunnerSyncWorker>()
                .setInitialDelay(0, TimeUnit.SECONDS)
                .build()

            WorkManager.getInstance(context)
                .enqueueUniqueWork("UNIQUE_RUNNER_SYNC", ExistingWorkPolicy.REPLACE, workRequest)
        }
    }
}
