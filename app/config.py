from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    database_hostname: str = os.getenv("DATABASE_HOSTNAME")
    database_port: str = os.getenv("DATABASE_PORT")
    database_password: str = os.getenv('DATABASE_PASSWORD')
    database_name: str = os.getenv('DATABASE_NAME')
    database_username: str = os.getenv('DATABASE_USERNAME')
    secret_key: str = os.getenv('SECRET_KEY')
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expire_minutes: int = ('ACCESS_TOKEN_EXPIRE_MINUTES')


settings = Settings()

