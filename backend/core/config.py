import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    PGPORT: str = os.getenv("POSTGRES_PORT")
    PGUSER: str = os.getenv("POSTGRES_USER")
    PGPASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # default postgres port is 5432
    PGHOST: str = os.getenv("POSTGRES_HOST", 5432)
    PGDATABASE: str = os.getenv("POSTGRES_DATABASE", "tdd")
    DATABASE_URL: str = os.getenv("POSTGRES_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    print(SECRET_KEY)
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 10
    TEST_USER_EMAIL = "test@example.com"


settings = Settings()
