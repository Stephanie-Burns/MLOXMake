import pytest
from pathlib import Path
from MLOXMaker.core.exceptions import (
    ErrorLevel, MLOXError, MLOXRuleError, InvalidRuleSyntaxError, MissingModError,
    CircularDependencyError, ConflictingRuleError, MLOXAPIError, NexusAPIFetchError,
    NexusRateLimitError, InvalidAPICredentials, ModMetadataParseError, MLOXIOError,
    MissingFileError, ExistingFileError, FilePermissionError, ExportFailureError,
    CorruptRuleFileError
)
from MLOXMaker.managers.app_log import AppLog, LogGroup, LogEvent

# Dummy logger that records log calls.
class DummyLogger:
    def __init__(self):
        self.calls = []
    def record(self, group, event, message, **kwargs):
        self.calls.append((group, event, message, kwargs))
    def reset(self):
        self.calls = []

# A fixture that patches AppLog logging methods to our dummy record.
@pytest.fixture(autouse=True)
def dummy_logger(monkeypatch):
    dummy = DummyLogger()
    monkeypatch.setattr(AppLog, "warning", dummy.record)
    monkeypatch.setattr(AppLog, "info", dummy.record)
    monkeypatch.setattr(AppLog, "error", dummy.record)
    return dummy

# Helper function to assert that the log call matches our expectations.
def assert_log(dummy, exc_instance, expected_details):
    # log_error() is called during __init__, so we expect one log call.
    assert len(dummy.calls) == 1, f"Expected 1 log call, got {len(dummy.calls)}"
    group, event, message, kwargs = dummy.calls[0]
    # Expected group and event.
    assert group == LogGroup.SYSTEM
    assert event == LogEvent.FAILED
    # Expected message: "<ExceptionClass>: <exception message>"
    expected_full_message = f"{exc_instance.__class__.__name__}: {exc_instance}"
    assert message == expected_full_message
    # The "terse" keyword should be set to the provided details.
    assert kwargs.get("terse") == expected_details
    dummy.reset()

def test_mlox_error(dummy_logger):
    e = MLOXError("test message", level=ErrorLevel.CRITICAL, details="detail")
    assert_log(dummy_logger, e, "detail")
    assert e.level == ErrorLevel.CRITICAL
    assert e.details == "detail"

def test_mlox_rule_error(dummy_logger):
    e = MLOXRuleError("rule error", level=ErrorLevel.CRITICAL, details="rule detail")
    assert_log(dummy_logger, e, "rule detail")

def test_invalid_rule_syntax_error(dummy_logger):
    e = InvalidRuleSyntaxError("foo")
    assert_log(dummy_logger, e, "Check rule formatting for errors.")

def test_missing_mod_error(dummy_logger):
    e = MissingModError("mod1")
    assert_log(dummy_logger, e, "Ensure the mod is installed or correctly referenced.")

def test_circular_dependency_error(dummy_logger):
    e = CircularDependencyError("mod2")
    assert_log(dummy_logger, e, "A mod depends on itself, directly or indirectly.")

def test_conflicting_rule_error(dummy_logger):
    e = ConflictingRuleError("ruleA", "ruleB")
    assert_log(dummy_logger, e, "Check rule definitions for logical contradictions.")

def test_mlox_api_error(dummy_logger):
    e = MLOXAPIError("api error", level=ErrorLevel.CRITICAL, details="api detail")
    assert_log(dummy_logger, e, "api detail")

def test_nexus_api_fetch_error(dummy_logger):
    e = NexusAPIFetchError("query")
    assert_log(dummy_logger, e, "Check API status or network connection.")

def test_nexus_rate_limit_error(dummy_logger):
    e = NexusRateLimitError()
    assert_log(dummy_logger, e, "Try again later or reduce request frequency.")

def test_invalid_api_credentials(dummy_logger):
    e = InvalidAPICredentials()
    assert_log(dummy_logger, e, "Ensure your API key is correctly configured.")

def test_mod_metadata_parse_error(dummy_logger):
    e = ModMetadataParseError("mod3")
    assert_log(dummy_logger, e, "API response may be malformed or incomplete.")

def test_mlox_io_error(dummy_logger):
    e = MLOXIOError("file.txt", "custom error", ErrorLevel.WARNING, "io detail")
    expected_message = f"MLOXIOError: custom error: {Path('file.txt')}"
    # The log message is generated from the exception’s __str__ (which is "custom error: file.txt")
    assert_log(dummy_logger, e, "io detail")
    assert isinstance(e.file_path, Path)
    assert e.file_path == Path("file.txt")

def test_mlox_io_error_with_path(dummy_logger):
    """Ensure MLOXIOError correctly handles Path objects."""
    e = MLOXIOError(Path("file.txt"), "custom error", ErrorLevel.WARNING, "io detail")
    assert isinstance(e.file_path, Path)
    assert e.file_path == Path("file.txt")
    assert_log(dummy_logger, e, "io detail")


def test_missing_file_error(dummy_logger):
    e = MissingFileError("missing.txt")
    expected_message = f"MissingFileError: File not found: {Path('missing.txt')}"
    assert_log(dummy_logger, e, "Ensure the file exists and is accessible.")
    assert e.file_path == Path("missing.txt")

def test_existing_file_error(dummy_logger):
    e = ExistingFileError("existing.txt")
    expected_message = f"ExistingFileError: File already exists: {Path('existing.txt')}"
    assert_log(dummy_logger, e, "Consider renaming or removing the existing file.")
    assert e.file_path == Path("existing.txt")

def test_file_permission_error(dummy_logger):
    e = FilePermissionError("protected.txt")
    expected_message = f"FilePermissionError: Insufficient permissions for file: {Path('protected.txt')}"
    assert_log(dummy_logger, e, "Check file permissions and try again.")
    assert e.file_path == Path("protected.txt")

def test_export_failure_error(dummy_logger):
    e = ExportFailureError("export.txt")
    expected_message = f"ExportFailureError: Failed to export rules: {Path('export.txt')}"
    assert_log(dummy_logger, e, "Ensure the file is writable and disk space is sufficient.")
    assert e.file_path == Path("export.txt")

def test_corrupt_rule_file_error(dummy_logger):
    e = CorruptRuleFileError("corrupt.txt")
    expected_message = f"CorruptRuleFileError: Corrupt rule file detected: {Path('corrupt.txt')}"
    assert_log(dummy_logger, e, "File may be incomplete or incorrectly formatted.")
    assert e.file_path == Path("corrupt.txt")
