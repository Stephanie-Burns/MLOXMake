
# **MLOXMaker Error Handling System (ERS) 🚀**
  
## **1️⃣ Overview & Strategy**

### **✅ Strategy**
- **Categorize errors** based on severity (**Warning, Recoverable, Critical**).
- **Use a base error class** (`MLOXError`) for consistency.
- **Provide actionable feedback** through clear messages.
- **Determine handling levels**:
  - **Method-Level** — Validate and raise predictable errors.
  - **Controller-Level** — Decide whether to retry, log, or escalate.
  - **Global Handler** — Catch unexpected errors to prevent crashes.

---

## **2️⃣ MLOXMaker Error Hierarchy 🌳**

```
📂 MLOXError
│
├── 📂 MLOXRuleError               [Issues with rule parsing/creation]
│   ├── 📄 InvalidRuleSyntaxError     : Rule is incorrectly formatted
│   ├── 📄 MissingModError            : Mod referenced in rule is not found
│   ├── 📄 CircularDependencyError    : Circular dependency detected in rules
│   ├── 📄 ConflictingRuleError       : Contradictory rules detected
│   └── 📄 UnresolvedDependencyError  : Missing required mod dependency
│
├── 📂 MLOXAPIError                [API & Data fetching issues]
│   ├── 📄 NexusAPIFetchError        : Failed to retrieve data from Nexus
│   ├── 📄 NexusRateLimitError       : Too many API requests (rate limited)
│   ├── 📄 NetworkError              : Internet connection issue
│   ├── 📄 InvalidAPICredentials     : API key is missing or invalid
│   └── 📄 ModMetadataParseError     : Failed to parse mod metadata
│
├── 📂 MLOXIOError                 [File & I/O operations]
│   ├── 📄 MissingFileError          : File not found
│   ├── 📄 ExistingFileError         : File already exists
│   ├── 📄 FilePermissionError       : No write access
│   ├── 📄 ConfigLoadError           : Failed to load config
│   ├── 📄 ExportFailureError        : Error saving rules to file
│   ├── 📄 ReadOnlyDirectoryError    : Cannot modify directory
│   └── 📄 CorruptRuleFileError      : Rule file is corrupted
```

---

## **3️⃣ Categorizing Errors**

| **Error Type**     | **Description**                                  | **Example**                                    | **Action**                                   |
|--------------------|------------------------------------------------|----------------------------------------------|----------------------------------------------|
| ⚠️ **Warning**     | Non-critical; operation continues             | A rule references a missing optional mod     | Log a warning; notify user subtly           |
| 🔄 **Recoverable** | Operation fails but app remains stable         | API request fails due to rate limits         | Retry with delay or notify the user         |
| ❌ **Critical**    | Major failures that prevent functionality      | Invalid rule file, database corruption       | Log, alert user, and halt execution if needed |

---

## **4️⃣ Base Error Class & Specific Types**

### **Base Error Class**

```python
class MLOXError(Exception):
    """Base class for all MLOXMaker errors."""

    def __init__(self, message, level="error", details=None):
        super().__init__(message)
        self.level = level  # "warning", "recoverable", "critical"
        self.details = details  # Extra debugging info or suggestions

    def log(self):
        """Logs the error using structured logging."""
        from mloxmaker.utils.logger import MLOXLogger
        log_methods = {
            "warning": MLOXLogger.warning,
            "recoverable": MLOXLogger.info,
            "critical": MLOXLogger.error
        }
        log_methods.get(self.level, MLOXLogger.error)(f"{self.__class__.__name__}: {self}", tag="ERROR")
```

### **Specific Error Types**
```python
class InvalidRuleSyntaxError(MLOXError):
    """Raised when a rule is incorrectly formatted."""
    def __init__(self, rule_text: str):
        super().__init__(f"Invalid rule syntax: {rule_text}", level="recoverable")

class MissingModError(MLOXError):
    """Raised when a rule references a mod that does not exist."""
    def __init__(self, mod_name: str):
        super().__init__(f"Mod not found: {mod_name}", level="recoverable")

class CircularDependencyError(MLOXError):
    """Raised when a circular dependency is detected in mod rules."""
    def __init__(self, mod_name: str):
        super().__init__(f"Circular dependency detected for: {mod_name}", level="critical")

class NexusAPIFetchError(MLOXError):
    """Raised when the Nexus Mods API fails to return a response."""
    def __init__(self, query: str):
        super().__init__(f"Failed to fetch data for: {query}", level="recoverable")
```

---

## **5️⃣ When to Raise vs. When to Log**

**Raise an Exception When:**
- A mod rule is completely invalid (e.g., **syntax error, missing required mods**).
- A **rule causes contradictions** (e.g., one mod both requiring and conflicting with another).
- A **circular dependency** is detected in the rule structure.

**Log (and do not raise) When:**
- A rule **references a missing mod**, but the rule is still valid.
- A **Nexus API request fails temporarily** (retrying may be possible).
- An export operation **succeeds partially**, but some rules could not be written.

---

## **6️⃣ Global Error Handler**

```python
import sys
from mloxmaker.utils.logger import MLOXLogger

def global_error_handler(exc_type, exc_value, exc_traceback):
    """Handles uncaught exceptions globally."""
    if isinstance(exc_value, MLOXError):
        exc_value.log()
    else:
        MLOXLogger.error(f"Unhandled Exception: {exc_value}", tag="ERROR")

sys.excepthook = global_error_handler  # Activate the global handler
```

---

## **7️⃣ Final Thoughts**
MLOXMaker’s ERS ensures:
- **Clear, actionable error messages**
- **Structured categorization** (warnings, recoverable, critical)
- **Method, controller, and global-level error handling**
- **Enhanced debugging and maintainability**

---

[Table of contents](index.md)
