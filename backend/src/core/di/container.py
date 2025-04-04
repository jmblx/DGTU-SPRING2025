from dishka import make_async_container
from dishka.integrations.fastapi import FastapiProvider

from core.di.providers.db import DBProvider
from core.di.providers.handlers import HandlerProvider
from core.di.providers.readers import ReaderProvider
from core.di.providers.redis_provider import RedisProvider
from core.di.providers.repositories import RepositoriesProvider
from core.di.providers.services import ServiceProvider
from core.di.providers.settings import SettingsProvider
from core.di.providers.uow import UowProvider

# from core.di.providers.usecases import UseCaseProvider


prod_provders = [
    DBProvider(),
    RedisProvider(),
    RepositoriesProvider(),
    SettingsProvider(),
    # UseCaseProvider(),
    ServiceProvider(),
    FastapiProvider(),
    HandlerProvider(),
    UowProvider(),
    ReaderProvider(),
]

container = make_async_container(*prod_provders)
