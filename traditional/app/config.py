from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    pguser: str = os.getenv("PGUSER")
    postgres_password = os.getenv("PGPASSWORD")
    railway_private_domain = os.getenv("RAILWAY_PRIVATE_DOMAIN")
    pgdatabase = os.getenv("PGDATABASE")
    database_private_url: str = os.getenv("DATABASE_PRIVATE_URL")
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


settings = Settings()
