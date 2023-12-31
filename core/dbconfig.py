from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.constants import DATABASE_URI


SQLALCHEMY_DB_URI = f"sqlite:///core/{DATABASE_URI}"

# create engine which creates a connection to the database and also facilitate for running of SQL on the DB
engine = create_engine(
    url=SQLALCHEMY_DB_URI,
    # echo=True,
    connect_args={"check_same_thread": False},
)

# create SessionLocal class to be used to instantiate and get sessions facilitate communication with database
SessionLocal = sessionmaker(
    bind=engine, autocommit=False, autoflush=False, expire_on_commit=False
)

# create Base class for app models to inherit from.
# Base = declarative_base(bind=engine)
Base = declarative_base()


# create a generator function to generate a session whenever called
# and can automatically close the session when no longer needed.
def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
