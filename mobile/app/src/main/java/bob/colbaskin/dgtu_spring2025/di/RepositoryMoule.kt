package bob.colbaskin.dgtu_spring2025.di

import bob.colbaskin.dgtu_spring2025.probabilities.data.remote.TablesRepositoryImpl
import bob.colbaskin.dgtu_spring2025.probabilities.domain.remote.TablesApiService
import bob.colbaskin.dgtu_spring2025.probabilities.domain.remote.TablesRepository
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

    @Provides
    @Singleton
    fun provideTablesApiService(retrofit: Retrofit): TablesApiService {
        return retrofit.create(TablesApiService::class.java)
    }

    @Provides
    @Singleton
    fun provideTablesRepository(tablesApiService: TablesApiService): TablesRepository {
        return TablesRepositoryImpl(tablesApiService)
    }
}