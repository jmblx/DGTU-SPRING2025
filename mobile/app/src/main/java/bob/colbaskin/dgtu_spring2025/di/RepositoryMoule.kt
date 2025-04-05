package bob.colbaskin.dgtu_spring2025.di


import bob.colbaskin.dgtu_spring2025.races.data.RaceRepositoryImpl
import bob.colbaskin.dgtu_spring2025.races.domain.RaceRepository
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent

@Module
@InstallIn(SingletonComponent::class)
object RepositoryModule {

    @Provides
    fun provideRaceRepository(): RaceRepository = RaceRepositoryImpl()
}