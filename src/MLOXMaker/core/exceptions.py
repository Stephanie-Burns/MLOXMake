from enum import StrEnum, auto
from pathlib import Path

from MLOXMaker.managers.app_log import AppLog, LogGroup, LogEvent

class ErrorLevel(StrEnum):
    """Defines severity levels for MLOXMaker errors."""
    WARNING = auto()       # ⚠️ Non-critical, operation continues
    RECOVERABLE = auto()   # 🔄 Operation failed but app remains stable
    CRITICAL = auto()      # ❌ Major failure, execution stops

class MLOXError(Exception):
    """Base class for all MLOXMaker errors, ensuring structured logging."""
    def __init__(self, message: str, level: ErrorLevel = ErrorLevel.CRITICAL, details: str | None = None):
        super().__init__(message)
        self.level = level
        self.details = details  # Optional debugging details
        self.log_error()

    def log_error(self):
        """Logs the error based on its severity level."""
        log_methods = {
            ErrorLevel.WARNING: AppLog.warning,
            ErrorLevel.RECOVERABLE: AppLog.info,
            ErrorLevel.CRITICAL: AppLog.error,
        }
        log_method = log_methods.get(self.level.lower(), AppLog.error)
        # noinspection PyArgumentList
        log_method(LogGroup.SYSTEM, LogEvent.FAILED, f"{self.__class__.__name__}: {self}", terse=self.details)


# ======================================================================================================================
#                                                                                                        ✅ Rule Errors
# ======================================================================================================================
class MLOXRuleError(MLOXError):
    """Base class for all rule-related errors."""
    pass
class InvalidRuleSyntaxError(MLOXRuleError):
    """Raised when a rule is incorrectly formatted."""
    def __init__(self, rule_text: str):
        super().__init__(
            message=f"Invalid rule syntax: {rule_text}", level=ErrorLevel.RECOVERABLE,
            details="Check rule formatting for errors."
        )

class MissingModError(MLOXRuleError):
    """Raised when a rule references a mod that does not exist."""
    def __init__(self, mod_name: str):
        super().__init__(
            f"Mod not found: {mod_name}", level=ErrorLevel.RECOVERABLE,
            details="Ensure the mod is installed or correctly referenced."
        )

class CircularDependencyError(MLOXRuleError):
    """Raised when a circular dependency is detected in mod rules."""
    def __init__(self, mod_name: str):
        super().__init__(
            message=f"Circular dependency detected for: {mod_name}", level=ErrorLevel.CRITICAL,
            details="A mod depends on itself, directly or indirectly."
        )

class ConflictingRuleError(MLOXRuleError):
    """Raised when contradictory rules are detected."""
    def __init__(self, rule_a: str, rule_b: str):
        super().__init__(
            message=f"Conflicting rules detected: {rule_a} <-> {rule_b}", level=ErrorLevel.CRITICAL,
            details="Check rule definitions for logical contradictions."
        )


# ======================================================================================================================
#                                                                                                         🌐 API Errors
# ======================================================================================================================
class MLOXAPIError(MLOXError):
    """Base class for all API-related errors."""
    pass

class NexusAPIFetchError(MLOXAPIError):
    """Raised when the Nexus Mods API fails to return a response."""
    def __init__(self, query: str):
        super().__init__(
            message=f"Failed to fetch data for: {query}", level=ErrorLevel.RECOVERABLE,
            details="Check API status or network connection."
        )

class NexusRateLimitError(MLOXAPIError):
    """Raised when the Nexus Mods API rate limit is exceeded."""
    def __init__(self):
        super().__init__(
            message="Nexus API rate limit exceeded.", level=ErrorLevel.WARNING,
            details="Try again later or reduce request frequency."
        )

class InvalidAPICredentials(MLOXAPIError):
    """Raised when the provided API key is invalid or missing."""
    def __init__(self):
        super().__init__(
            message="Invalid or missing Nexus API key.", level=ErrorLevel.CRITICAL,
            details="Ensure your API key is correctly configured."
        )

class ModMetadataParseError(MLOXAPIError):
    """Raised when mod metadata from the API fails to parse correctly."""
    def __init__(self, mod_name: str):
        super().__init__(
            message=f"Failed to parse metadata for mod: {mod_name}", level=ErrorLevel.RECOVERABLE,
            details="API response may be malformed or incomplete."
        )


# ======================================================================================================================
#                                                                                                          📂 IO Errors
# ======================================================================================================================
class MLOXIOError(MLOXError):
    """Base class for all file-related errors, enforcing pathlib paths."""
    def __init__(self, file_path: str | Path, message: str, level: ErrorLevel, details: str | None = None):
        self.file_path = Path(file_path)
        super().__init__(f"{message}: {self.file_path}", level=level, details=details)

class MissingFileError(MLOXIOError):
    """Raised when a required file is missing."""
    def __init__(self, file_path: str):
        super().__init__(
            file_path, message="File not found", level=ErrorLevel.CRITICAL,
            details="Ensure the file exists and is accessible."
        )

class ExistingFileError(MLOXIOError):
    """Raised when trying to overwrite an existing file without permission."""
    def __init__(self, file_path: str):
        super().__init__(
            file_path, message="File already exists", level=ErrorLevel.WARNING,
            details="Consider renaming or removing the existing file."
        )

class FilePermissionError(MLOXIOError):
    """Raised when lacking permission to read/write a file."""
    def __init__(self, file_path: str):
        super().__init__(
            file_path, message="Insufficient permissions for file", level=ErrorLevel.CRITICAL,
            details="Check file permissions and try again."
        )

class ExportFailureError(MLOXIOError):
    """Raised when exporting rules to a file fails."""
    def __init__(self, file_path: str):
        super().__init__(
            file_path, message="Failed to export rules", level=ErrorLevel.RECOVERABLE,
            details="Ensure the file is writable and disk space is sufficient."
        )

class CorruptRuleFileError(MLOXIOError):
    """Raised when a rule file is detected as corrupted."""
    def __init__(self, file_path: str):
        super().__init__(
            file_path, message="Corrupt rule file detected", level=ErrorLevel.CRITICAL,
            details="File may be incomplete or incorrectly formatted."
        )
