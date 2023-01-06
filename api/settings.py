from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):

    database_url: str = "sqlite:///db.sqlite3"
    secret_key: str
    algorithm: str = 'HS256'
    expiration: int = 5000


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
