# settings.py
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID", cast=Secret)
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN", cast=Secret)
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER", cast=Secret)

SMTP_SERVER = config("SMTP_SERVER", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=int)
SMTP_USERNAME = config("SMTP_USERNAME", cast=Secret)
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=Secret)


