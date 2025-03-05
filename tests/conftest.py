import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from MLOXMaker.database.db import Base, engine, SessionLocal
from MLOXMaker.database.manager import DatabaseManager
from MLOXMaker.managers.app_log import AppLog

def pytest_configure(config):
    """Automatically enable test mode in AppLog when pytest runs."""
    AppLog.testing_mode = True

# Override the database settings by patching the Settings class.
@pytest.fixture(scope="session", autouse=True)
def override_database_settings():
    from MLOXMaker.config.settings import Settings
    mp = pytest.MonkeyPatch()
    # Set DATABASE_PATH on the Settings class to ":memory:"
    mp.setattr(Settings, "DATABASE_PATH", ":memory:")
    yield
    mp.undo()

# Rebind the engine to an in-memory database.
@pytest.fixture(scope="session", autouse=True)
def rebind_db_engine(override_database_settings):
    import MLOXMaker.database.db as db_mod
    new_engine = create_engine("sqlite:///:memory:", future=True)
    # Dispose of the old engine and reassign to the new in-memory engine.
    db_mod.engine.dispose()
    db_mod.engine = new_engine
    # Reconfigure SessionLocal to use the new engine.
    SessionLocal.configure(bind=new_engine)
    Base.metadata.create_all(bind=new_engine)
    yield
    Base.metadata.drop_all(bind=new_engine)

# Define test_db fixture so that tests can get a fresh session.
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """
    Creates a new in-memory database for each test.
    """
    engine = create_engine(TEST_DATABASE_URL, future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

# Clear the database between tests to ensure a clean state.
@pytest.fixture(autouse=True)
def clear_db():
    from MLOXMaker.database.db import Base, engine
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
    yield
    with engine.begin() as connection:
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(table.delete())
    DatabaseManager.initialize()
