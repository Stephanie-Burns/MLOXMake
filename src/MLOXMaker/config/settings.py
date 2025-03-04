from pathlib import Path


class Settings:
    """Default application settings."""

    # 🔹 General Config
    APP_NAME = "MLOXMaker"
    VERSION = "0.1.0"

    # 🔹 Logging
    LOGGER_NAME = "MLOXMaker"
    LOG_LEVEL = "INFO"
    LOG_FILE_PATH = Path.home() / ".config" / "mloxmaker" / "mloxmaker.log"
    TOGGLE_STDOUT_LOGGING = True
    TOGGLE_FILE_LOGGING = False

    # 🔹 Database
    DATABASE_PATH = Path.home() / ".config" / "mloxmaker" / "mloxmaker.db"

    # 🔹 UI Settings
    THEME = "dark"
    WINDOW_SIZE = (1280, 720)

    # 🔹 Feature Toggles
    ENABLE_CLI_MODE = True
    ENABLE_EVENT_DEBUGGING = False

    @classmethod
    def ensure_dirs(cls):
        """Ensure required directories exist."""
        cls.LOG_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

Settings.ensure_dirs()
