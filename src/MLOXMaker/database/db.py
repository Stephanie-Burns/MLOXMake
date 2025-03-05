
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from MLOXMaker.config.settings import Settings
from pathlib import Path

DATABASE_URL = f"sqlite:///{Settings.DATABASE_PATH}"

# Ensure database directory exists
Path(Settings.DATABASE_PATH).parent.mkdir(parents=True, exist_ok=True)

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def initialize():
    """Initialize the database (create tables if needed)."""
    from MLOXMaker.database.models import Rule, Mod, Dependency  # Import models
    Base.metadata.create_all(bind=engine)
