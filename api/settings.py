from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    database_url: str
    secret_key: str
    algorithm: str = 'HS256'
    expiration: int = 5000
    base_dir: Path = Path(__file__).resolve().parent.parent


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
