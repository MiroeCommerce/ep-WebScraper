"""Database connection and session management.

This module sets up the SQLAlchemy engine and session factory for the
application. It reads the database connection string from the core
configuration and provides a declarative base class for ORM models.

Typical Usage:
    from data_ingestion_service.app.core.database import SessionLocal, Base
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings  # Correctly import the settings object

# Create the SQLAlchemy engine using the database URL from the settings.
# The engine is the entry point to the database and handles the connection pool.
engine = create_engine(settings.DATABASE_URL)

# Create a session factory. This configured Session class will be used to
# create new database sessions for transactions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a declarative base class. All ORM models in the application
# will inherit from this class.
Base = declarative_base()