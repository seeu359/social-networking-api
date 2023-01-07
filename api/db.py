from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.settings import settings

db_connect = settings.database_prefix + str(settings.base_dir) + '/db.sqlite3'
engine = create_engine(db_connect)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
