from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.settings import settings

engine = create_engine(settings.database_url)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
