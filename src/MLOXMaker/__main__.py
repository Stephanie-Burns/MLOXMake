import sys
from MLOXMaker.config.settings import Settings
from MLOXMaker.managers.app_log import AppLog, LogGroup, LogEvent
# from MLOXMaker.database.db import Database  # Placeholder for upcoming DB setup

def main():
    """MLOXMaker entry point."""
    AppLog.setup_logger()
    AppLog.info(LogGroup.SYSTEM, LogEvent.STARTED, "MLOXMaker is starting up.")

    # Ensure database is ready
    # Database.initialize()  # Placeholder for later

    # Check if running in CLI mode
    if len(sys.argv) > 1:   # and Settings.ENABLE_CLI_MODE:
        from MLOXMaker.cli import cli_main  # Placeholder for CLI implementation
        cli_main()
    else:
        # from MLOXMaker.ui.app import run_ui  # Placeholder for PySide UI
        # run_ui()
        ...
    AppLog.info(LogGroup.SYSTEM, LogEvent.COMPLETED, "MLOXMaker is shutting down.")

if __name__ == "__main__":
    main()
