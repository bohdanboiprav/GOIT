# import pydantic
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    django_secret_key: str
    db_engine: str
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    mongo_db_name: str
    mongo_host: str
    email_host: str
    email_port: int
    email_host_user: str
    email_host_password: str
    mail_from: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
