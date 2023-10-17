import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Job Board"
    PROJECT_VERSION: str = "1.0.0"

    PGPORT: str = os.getenv("PGPORT")
    PGUSER: str = os.getenv("PGUSER")
    PGPASSWORD = os.getenv("PGPASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    # default postgres port is 5432
    PGHOST: str = os.getenv("PGHOST", 5432)
    PGDATABASE: str = os.getenv("PGDATABASE", "tdd")
    DATABASE_URL: str = "postgres://jo_hywb_user:LV5C4um0j8NOhvANSslJ4URL2WYcRHNs@dpg-ckndtpf83ejs73fp8q40-a/jo_hywb"
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    TEST_USER_EMAIL = "test@example.com"


settings = Settings()
