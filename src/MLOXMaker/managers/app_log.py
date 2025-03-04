"""
App Logger Module
=====================

This module provides a centralized, structured logging system for your application.
It uses a custom configuration (via LogConfig) to initialize a static logger that outputs
messages to one or more handlers (console and/or file). All log messages are grouped with a
"group" and an "event" (using LogGroup and LogEvent enums) and are formatted using a custom
formatter that injects emojis and aligned spacing.

Key Design Decisions:
- **Static Logger Reference:**
  The logger is stored as a static class attribute (AppLog.logger) so that every log message
  uses the same configured logger.
- **Structured Logging:**
  Log messages include extra metadata ("group" and "event") that are enforced by the AppLog wrapper
  methods (info, warning, error, etc.). This ensures consistency in log output.
- **Flexible Configuration:**
  Log Settings are read from the application's Settings (using keys POST_STDOUT, POST_DISK, and
  LOG_FILE_PATH) via the LogConfig dataclass.
- **Handler Management:**
  The module provides methods to enable or disable file and console logging. When enabling file
  logging, it ensures that the log file's parent directory exists and opens the file in append mode.
- **Prevention of Recursion:**
  During setup, log messages that indicate the logger’s state are sent directly through the static
  logger reference (AppLog.logger) to avoid recursive calls to the wrapper methods.

Usage:
    Call AppLog.setup_logger() early in your application to initialize the logging system.
    Then use AppLog.info(), AppLog.error(), etc., throughout your code to log messages with structured metadata.

Happy logging!
"""

import logging
import os
import sys
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path
from typing import Optional

try:
    from MLOXMaker.config.settings import Settings
except ImportError as e:
    Settings = None
    print(f"⚠️ Failed to import settings: {e}")


# ======================================================================================================================
#                                                                                                             🔥 Logger
# ======================================================================================================================


@dataclass
class LogConfig:
    """Configuration object for app logging."""
    logger_name: str                = "APP_LOGGER"
    log_level: str                  = "DEBUG"
    toggle_console_logging: bool    = True
    toggle_file_logging: bool       = False
    log_file_path: Path             = Path.home() / "app.log"

    @classmethod
    def from_settings(cls):
        """Creates a LogConfig object from application settings."""
        return cls(
            logger_name             =getattr(Settings, "LOGGER_NAME", "APP_LOGGER"),
            log_level               =getattr(Settings, "LOG_LEVEL", "DEBUG").upper(),
            toggle_console_logging  =getattr(Settings, "TOGGLE_STDOUT_LOGGING", True),
            toggle_file_logging     =getattr(Settings, "TOGGLE_FILE_LOGGING", False),
            log_file_path           =Path(getattr(Settings, "LOG_FILE_PATH", Path.home() / "app.log"))
        )

class LogGroup(StrEnum):
    """Logging categories used to group related log messages."""
    FILE                = auto()        # File operations (e.g., reading, writing)
    ARCHIVE             = auto()        # Archiving and extraction processes
    SYSTEM              = auto()        # General system-related events


class LogEvent(StrEnum):
    """Specific events that can be logged."""
    STARTED             = auto()        # An operation has started
    COMPLETED           = auto()        # An operation has successfully completed
    FAILED              = auto()        # An operation has failed


class AppLog:
    """Centralized logger with structured groups & events.

    All logging should be performed through the AppLog wrapper methods (info, error, etc.)
    to ensure that log messages are tagged with a group and event, and are formatted consistently
    using the custom formatter.
    """
    _config: LogConfig | None = None
    _initialized: bool = False

    # Static reference to the logger.
    logger: Optional[logging.Logger] = None

    class Level(StrEnum):
        """Logging severity levels (specific to AppLog)."""
        DEBUG           = auto()        # Detailed debugging information
        INFO            = auto()        # General informational messages
        WARNING         = auto()        # Non-critical issues that might require attention
        ERROR           = auto()        # Recoverable errors
        CRITICAL        = auto()        # Critical failures that may crash the application

    EMOJIS = {
        Level.DEBUG     : "🛠",
        Level.INFO      : "⬜",
        Level.WARNING   : "🟨",
        Level.ERROR     : "🟥",
        Level.CRITICAL  : "💣",
    }

    @classmethod
    def setup_logger(cls, config: Optional[LogConfig] = None):
        """Configures the app logger based on Settings.

        This method initializes the logger only once. It sets the logger level,
        adds file and console handlers according to the configuration, and logs
        an initialization message directly through the static logger reference.
        """
        if cls._initialized:
            return  # Only initialize once.

        cls._config = config or LogConfig.from_settings()
        cls.logger = logging.getLogger(cls._config.logger_name)
        cls.logger.handlers.clear()
        cls.logger.propagate = False  # Prevent messages from propagating to the root logger.

        cls.logger.setLevel(getattr(logging, cls._config.log_level.upper(), logging.DEBUG))

        if cls._config.toggle_file_logging:
            cls.toggle_file_logging(True, cls._config.log_file_path)
        if cls._config.toggle_console_logging:
            cls.toggle_console_logging(True, cls.logger)

        cls._initialized = True

        # Log the initialization message directly using the static logger.
        cls.logger.info("Logging system initialized.",
                        extra={"group": LogGroup.SYSTEM, "event": LogEvent.COMPLETED})

    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Returns the static logger instance, initializing it if necessary."""
        if not cls._initialized:
            cls.setup_logger()
        return cls.logger

    @classmethod
    def toggle_file_logging(cls, enabled: bool, file_path: Optional[Path] = None):
        """Enables or disables file logging, allowing users to specify a file path."""
        logger = cls.logger or logging.getLogger("APP_LOGGER")
        cls._remove_handlers(logger, logging.FileHandler)

        if enabled:
            log_path = Path(file_path) if isinstance(file_path, (str, Path)) else Path.home() / "app.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(str(log_path), mode='a', encoding="utf-8")
            cls._add_handler(logger, file_handler, AppLogFormatter(datefmt="%Y-%m-%d %H:%M:%S"))
            logger.info(
                f"File logging enabled at {log_path} → Hello file! :)",
                extra={"group": LogGroup.SYSTEM, "event": LogEvent.COMPLETED}
            )
        else:
            logger.info(
                "File logging disabled → Goodbye file! :)",
                extra={"group": LogGroup.SYSTEM, "event": LogEvent.COMPLETED}
            )

    @staticmethod
    def toggle_console_logging(enabled: bool, logger: logging.Logger = None):
        """Enables or disables console logging, ensuring correct separation of stdout and stderr."""
        logger = logger or logging.getLogger("APP_LOGGER")

        # Remove existing StreamHandlers
        for handler in logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                logger.removeHandler(handler)

        if enabled:
            # Normal logs (INFO, DEBUG) → stdout
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.DEBUG)  # Includes INFO & DEBUG
            AppLog._add_handler(logger, stdout_handler, AppLogFormatter(datefmt="%Y-%m-%d %H:%M:%S"))

            # Warnings & Errors → stderr
            stderr_handler = logging.StreamHandler(sys.stderr)
            stderr_handler.setLevel(logging.WARNING)  # Includes WARNING, ERROR, CRITICAL
            AppLog._add_handler(logger, stderr_handler, AppLogFormatter(datefmt="%Y-%m-%d %H:%M:%S"))

            logger.info("Console logging enabled → stdout for info, stderr for errors",
                        extra={"group": LogGroup.SYSTEM, "event": LogEvent.COMPLETED})
        else:
            logger.info("Console logging disabled",
                        extra={"group": LogGroup.SYSTEM, "event": LogEvent.COMPLETED})

    @classmethod
    def set_log_level(cls, new_level: str, logger: logging.Logger = None):
        """Dynamically sets the global log level for the provided logger (or defaults to the app logger)."""
        logger = logger or cls.get_logger()
        logger.setLevel(getattr(logging, new_level.upper(), logging.DEBUG))
        cls.info(
            LogGroup.SYSTEM, LogEvent.COMPLETED, f"Log level set to {new_level.upper()}",
            terse="Log level updated."
        )

    @classmethod
    def info(cls, group: LogGroup, event: LogEvent, report: str, *, terse: Optional[str] = None):
        """Logs an informational message (normal operation)."""
        cls._log(group, event, report, terse=terse, level=cls.Level.INFO)

    @classmethod
    def warning(cls, group: LogGroup, event: LogEvent, report: str, *, terse: Optional[str] = None):
        """Logs a warning message (non-critical issue)."""
        cls._log(group, event, report, terse=terse, level=cls.Level.WARNING)

    @classmethod
    def error(cls, group: LogGroup, event: LogEvent, report: str, *, terse: Optional[str] = None):
        """Logs an error message (critical issue encountered)."""
        cls._log(group, event, report, terse=terse, level=cls.Level.ERROR)

    @classmethod
    def debug(cls, group: LogGroup, event: LogEvent, report: str, *, terse: Optional[str] = None):
        """Logs a debug message (detailed diagnostic information)."""
        cls._log(group, event, report, terse=terse, level=cls.Level.DEBUG)

    @classmethod
    def critical(cls, group: LogGroup, event: LogEvent, report: str, *, terse: Optional[str] = None):
        """Logs a critical message (severe error causing potential shutdown)."""
        cls._log(group, event, report, terse=terse, level=cls.Level.CRITICAL)

    @classmethod
    def _log(
            cls, group: LogGroup, event: LogEvent, report: str,
            terse: Optional[str] = None, level: "AppLog.Level" = Level.INFO
    ):
        """
        (Private) Logs a structured message while enforcing valid groups & events.
        This method is for internal use only.
        """
        logger = cls.get_logger()
        log_method = getattr(logger, level.name.lower(), logger.info)
        formatted_message = f"{report} {'→ ' + terse if terse else ''}"
        log_method(formatted_message, extra={"group": group, "event": event})

    @staticmethod
    def _add_handler(logger: logging.Logger, handler: logging.Handler, formatter: logging.Formatter):
        """(Private) Adds a formatted handler to the logger."""
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    @staticmethod
    def _remove_handlers(logger: logging.Logger, handler_type: type[logging.Handler]):
        """(Private) Removes all handlers of a specific type from the logger."""
        for handler in logger.handlers[:]:
            if isinstance(handler, handler_type):
                logger.removeHandler(handler)


# ======================================================================================================================
#                                                                                                         🎨 Formatters
# ======================================================================================================================
class AppLogFormatter(logging.Formatter):
    """Custom formatter to inject emojis and groups into log output with aligned spacing."""
    LEVEL_WIDTH     = 9
    TAG_WIDTH       = 10
    EVENT_WIDTH     = 11

    def format(self, record: logging.LogRecord) -> str:
        record.emoji = AppLog.EMOJIS.get(getattr(AppLog.Level, record.levelname.upper(), AppLog.Level.INFO), "")
        record.group = getattr(record, "group", "UNKNOWN")
        record.event = getattr(record, "event", "UNKNOWN")
        record.asctime = self.formatTime(record, self.datefmt)

        level_string = self.format_spec(record.levelname, self.LEVEL_WIDTH)
        group_string = self.format_spec(record.group, self.TAG_WIDTH)
        event_string = self.format_spec(record.event, self.EVENT_WIDTH)
        logger_message = record.getMessage()

        if "PYTEST_CURRENT_TEST" in os.environ and sys.stdout.tell() == 0:
            print(flush=True)
        return (
            f"{record.emoji} {level_string.upper()} {group_string.upper()} "
            f"{event_string.upper()} {record.asctime} - {logger_message}"
        )

    @staticmethod
    def format_spec(value, width):
        return f"[{value:<{width - 2}}]"
