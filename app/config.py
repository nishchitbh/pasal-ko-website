from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    pguser: str = os.getenv("PGUSER")
    postgres_password = os.getenv("POSTGRES_PASSWORD")
    railway_private_domain = os.getenv("RAILWAY_PRIVATE_DOMAIN")
    pgdatabase = os.getenv("PGDATABASE")
    database_private_url: str = f"postgresql://{pguser}:{postgres_password}@{railway_private_domain}:5432/{pgdatabase}"
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = "ACCESS_TOKEN_EXPIRE_MINUTES"


settings = Settings()
print(settings.database_private_url)
