import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    secret_key: str
    algorithm: str = 'HS256'
    expiration: int = 5000
    base_dir: Path = Path(__file__).resolve().parent.parent
    database_url: str
    test_database_url: str = 'sqlite:///' + os.path.join(
        str(base_dir) + '/tests/test_db.sqlite3'
    )
    test_database_path: str = os.path.join(
        str(base_dir) + '/tests/test_db.sqlite3'
    )


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
