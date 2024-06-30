# settings.py
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)


