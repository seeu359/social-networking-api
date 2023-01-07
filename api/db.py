from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3')

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
