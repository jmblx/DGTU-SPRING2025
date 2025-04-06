package bob.colbaskin.dgtu_spring2025.di


import bob.colbaskin.dgtu_spring2025.races.data.remote.RaceRepositoryImpl
import bob.colbaskin.dgtu_spring2025.races.data.remote.RunnerRepositoryImpl
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RaceRepository
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerApiService
import bob.colbaskin.dgtu_spring2025.races.domain.remote.RunnerRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.components.SingletonComponent

import retrofit2.Retrofit
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {

    @Provides
    @Singleton
    fun provideRaceRepository(): RaceRepository = RaceRepositoryImpl()

    @Provides
    @Singleton
    fun provideRunnerApiService(retrofit: Retrofit): RunnerApiService {
        return retrofit.create(RunnerApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideRunnerRepository(runnerApiService: RunnerApiService): RunnerRepository {
        return RunnerRepositoryImpl(runnerApiService)
    }
}