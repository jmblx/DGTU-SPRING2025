from dishka import Provider, Scope, provide


class SettingsProvider(Provider):
    ...
    # firebase_config = provide(FirebaseConfig().from_env, scope=Scope.APP, provides=FirebaseConfig
