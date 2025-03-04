import logging
from MLOXMaker.config.settings import Settings
from MLOXMaker.managers.app_log import AppLogFormatter, AppLog, LogGroup, LogEvent
import pytest

@pytest.fixture(autouse=True)
def override_settings(monkeypatch):
    monkeypatch.setattr(Settings, "LOGGER_NAME", "APP_LOGGER")
    monkeypatch.setattr(Settings, "LOG_LEVEL", "DEBUG")

def create_test_record(message, level=logging.INFO, tag="UNIT", event="COMPLETED"):
    """
    🏗️ Creates a test log record for validation.

    🔹 Simulates an actual log entry with a custom message, log level, tag, and event.
    """
    record = logging.LogRecord(
        name="APP_LOGGER",
        level=level,
        pathname=__file__,
        lineno=10,
        msg=message,
        args=(),
        exc_info=None
    )
    record.tag = tag
    record.event = event
    return record


def test_log_formatter():
    """
    🎨 Tests the custom AppLogFormatter.

    🔹 Steps:
    1️⃣ Creates a test log record with a sample message.
    2️⃣ Formats it using `AppLogFormatter`.
    3️⃣ Ensures the formatted output includes:
       - The correct log level emoji.
       - The `[INFO]` log tag.
       - The `[COMPLETED]` event.
       - The original message.
    """
    formatter = AppLogFormatter(datefmt="%Y-%m-%d %H:%M:%S")
    record = create_test_record("This is a test message")
    formatted = formatter.format(record)

    assert "⬜" in formatted  # INFO level emoji
    assert "[INFO" in formatted  # Log level
    assert "[COMPLETED" in formatted  # Event tag
    assert "This is a test message" in formatted  # Message content


def test_set_log_level():
    """
    📡 Tests AppLog.set_log_level().

    🔹 Steps:
    1️⃣ Sets the log level to `ERROR` and verifies the logger updates.
    2️⃣ Sets the log level to `DEBUG` and verifies the change.
    """
    AppLog.set_log_level("ERROR")
    assert logging.getLogger("APP_LOGGER").level == logging.ERROR

    AppLog.set_log_level("DEBUG")
    assert logging.getLogger("APP_LOGGER").level == logging.DEBUG


def test_toggle_stdout_logging(capsys):
    """
    📢 Tests toggling console logging on and off.

    🔹 Steps:
    1️⃣ Disable console logging and verify no output is captured.
    2️⃣ Enable console logging and verify expected output appears.
    """
    AppLog.toggle_console_logging(False)
    AppLog.info(
        group=LogGroup.SYSTEM,
        event=LogEvent.COMPLETED,
        report="Test console logging disabled",
        terse="No output expected"
    )

    captured = capsys.readouterr()
    output = captured.out[1:] if captured.out.startswith("\n") else captured.out
    assert (output + captured.err) == ""  # Should capture nothing

    AppLog.toggle_console_logging(True)
    AppLog.info(
        group=LogGroup.SYSTEM,
        event=LogEvent.COMPLETED,
        report="Test console logging enabled",
        terse="Output expected"
    )

    captured = capsys.readouterr()
    assert "Test console logging enabled" in (captured.out + captured.err)


def test_enable_file_logging(tmp_path):
    """
    📂 Tests file logging.

    🔹 Steps:
    1️⃣ Create a custom logger configuration with a temporary file.
    2️⃣ Reinitialize `AppLog` with the new config.
    3️⃣ Write a test log message and flush handlers.
    4️⃣ Verify that the log file contains the expected entry.
    5️⃣ Clean up by disabling file logging.
    """
    from MLOXMaker.managers.app_log import LogConfig

    # Set up logging with a temporary test file
    custom_config = LogConfig(
        logger_name="APP_LOGGER",
        log_level="DEBUG",
        toggle_console_logging=True,
        toggle_file_logging=True,
        log_file_path=tmp_path / "test_app.log"
    )

    AppLog._initialized = False  # Reset logger
    AppLog.setup_logger(config=custom_config)

    AppLog.info(
        group=LogGroup.SYSTEM,
        event=LogEvent.COMPLETED,
        report="Test file logging",
        terse="File logging test"
    )

    log_file = custom_config.log_file_path

    # Ensure data is written before reading
    for handler in logging.getLogger("APP_LOGGER").handlers:
        if isinstance(handler, logging.FileHandler):
            handler.flush()

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "File logging enabled at" in content  # Ensure logging was written

    AppLog.toggle_file_logging(False)  # Clean up

def test_all_log_levels(capsys, monkeypatch):
    """
    🎭 Tests that **all log levels** produce the expected output.

    🔹 Steps:
    1️⃣ Remove the `PYTEST_CURRENT_TEST` env var to prevent formatting issues.
    2️⃣ Enable console logging and flush existing output.
    3️⃣ Log messages at **all severity levels**.
    4️⃣ Capture the output and verify:
       - The correct **emoji** is present for each level.
       - Both `report` and `terse` messages are included.
    """
    # Prevent pytest from adding extra newlines
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)

    # Enable console logging and flush existing output
    AppLog.toggle_console_logging(True)
    capsys.readouterr()  # Clear any prior output

    # Log messages at different levels
    AppLog.debug(group=LogGroup.SYSTEM, event=LogEvent.COMPLETED, report="Test debug", terse="Debug test")
    AppLog.info(group=LogGroup.SYSTEM, event=LogEvent.COMPLETED, report="Test info", terse="Info test")
    AppLog.warning(group=LogGroup.SYSTEM, event=LogEvent.COMPLETED, report="Test warning", terse="Warning test")
    AppLog.error(group=LogGroup.SYSTEM, event=LogEvent.COMPLETED, report="Test error", terse="Error test")
    AppLog.critical(group=LogGroup.SYSTEM, event=LogEvent.COMPLETED, report="Test critical", terse="Critical test")

    # Capture both stdout and stderr
    captured = capsys.readouterr()
    output = captured.out + captured.err

    # Verify emojis for each log level
    assert "🛠" in output, "Debug emoji not found"
    assert "⬜" in output, "Info emoji not found"
    assert "🟨" in output, "Warning emoji not found"
    assert "🟥" in output, "Error emoji not found"
    assert "💣" in output, "Critical emoji not found"

    # Verify log messages
    assert "Test debug" in output and "Debug test" in output
    assert "Test info" in output and "Info test" in output
    assert "Test warning" in output and "Warning test" in output
    assert "Test error" in output and "Error test" in output
    assert "Test critical" in output and "Critical test" in output

def test_setup_logger_already_initialized():
    """
    🚀 Tests that `setup_logger()` returns immediately when already initialized.

    🔹 Steps:
    1️⃣ Manually set `_initialized` to `True`.
    2️⃣ Store the current logger instance.
    3️⃣ Call `setup_logger()`, which should **exit early** without modifications.
    4️⃣ Verify that the logger instance remains unchanged.
    """
    # Simulate an already initialized logger
    AppLog._initialized = True
    original_logger = logging.getLogger("APP_LOGGER")
    AppLog.logger = original_logger

    # Call setup_logger (should do nothing)
    AppLog.setup_logger()

    # Ensure the logger hasn't changed
    assert AppLog.logger is original_logger


def test_get_logger_invokes_setup():
    """
    🏗️ Tests that `get_logger()` triggers `setup_logger()` when uninitialized.

    🔹 Steps:
    1️⃣ Ensure `_initialized` is `False` and `logger` is `None`.
    2️⃣ Call `get_logger()`, which should **internally call `setup_logger()`**.
    3️⃣ Verify that `get_logger()` now returns a valid logger.
    4️⃣ Ensure `_initialized` is now `True`.
    """
    # Reset logger state
    AppLog._initialized = False
    AppLog.logger = None

    # Call get_logger(), should initialize
    logger = AppLog.get_logger()

    assert logger is not None, "Logger should be initialized"
    assert AppLog._initialized is True, "AppLog should be marked as initialized"



def test_remove_handlers():
    """
    🧹 Tests that `_remove_handlers()` properly removes handlers of a specific type.

    🔹 Steps:
    1️⃣ Add a test `StreamHandler` to the logger.
    2️⃣ Call `_remove_handlers()` targeting `StreamHandler`.
    3️⃣ Ensure the handler is **removed**.
    """
    logger = logging.getLogger("APP_LOGGER")

    # Add a test handler
    test_handler = logging.StreamHandler()
    logger.addHandler(test_handler)

    # Verify handler was added
    assert any(isinstance(h, logging.StreamHandler) for h in logger.handlers), "Handler should exist before removal"

    # Call remove method
    AppLog._remove_handlers(logger, logging.StreamHandler)

    # Verify handler was removed
    assert not any(isinstance(h, logging.StreamHandler) for h in logger.handlers), "Handler should be removed"
