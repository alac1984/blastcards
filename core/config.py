import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "Blastcards!"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: Optional[str] = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    DATABASE_URL: str = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30


settings = Settings()
