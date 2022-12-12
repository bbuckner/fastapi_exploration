from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .config import settings

# ORMS are good for Create, Update, Delete
# as well as small Reads.
# RAW SQL is better for large reads (even
# if simple query) and/or complex sql queries.

# format of a database connection url:
# postgresql+<driver>://<username>:<password>@<ip-address>/<hostname>/<database_name>
# The plus sign and <driver> part of the url are optional.

SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}"
    f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)
engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
