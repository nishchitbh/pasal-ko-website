from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# Database URL from the environment variable
SQLALCHEMY_DATABASE_URL = settings.database_private_url

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Create a session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base for SQLAlchemy models
Base = declarative_base()


def get_db():
    """Gets the database session.
    Returns:
        db: database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
