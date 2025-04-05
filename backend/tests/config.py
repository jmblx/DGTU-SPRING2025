import tomllib
from pathlib import Path

config_path = Path(__file__).parent.parent / "config" / "test_config.toml"

with open(config_path, "rb") as f:
    config = tomllib.load(f)

db = config["database"]

TEST_DATABASE_URI = (
    f"postgresql+asyncpg://{db['user']}:{db['password']}@"
    f"{db['host']}:{db['port']}/{db['name']}"
)
