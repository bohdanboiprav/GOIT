from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_SERVER_PUBLIC_KEY: str
    AWS_SERVER_SECRET_KEY: str
    AWS_REGION: str

    model_config = ConfigDict(extra='ignore', env_file=".env", env_file_encoding="utf-8") # noqa


settings = Settings()
