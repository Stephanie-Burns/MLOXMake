
[Table of contents](index.md)


# **MLOXMaker Logging System 🚀**

## **1️⃣ Overview**
MLOXMaker’s logging system ensures **structured, readable, and maintainable logs** that track **mod rule operations, API requests, and system events**. 

✅ **Why this matters:**  
- **Debugging & Transparency** → Quickly diagnose rule conflicts, Nexus API failures, or file issues.  
- **Consistency** → Prevent unstructured messages by enforcing predefined log categories & events.  
- **Performance** → Log efficiently without excessive verbosity.  

---

## **2️⃣ Logging Groups & Events**

### **Logging Groups (`group`)**
| Group         | Purpose |
|--------------|---------|
| `RULES`      | Mod rule creation, validation, and conflicts |
| `API`        | Nexus Mods API requests & responses |
| `FILE`       | File operations (saving, exporting, reading rules) |
| `SYSTEM`     | General app/system-wide events |

### **Logging Events (`event`)**
| Event         | Purpose |
|--------------|---------|
| `STARTED`    | Process has begun |
| `COMPLETED`  | Process finished successfully |
| `FAILED`     | Process encountered an error |
| `VALIDATED`  | A rule or file was checked and found valid |
| `MISSING`    | Something required was not found |

✅ **Events are extendable** as the tool grows.

---

## **3️⃣ How to Use `MLOXLogger`**

### **✅ Correct Logging Example**
```python
MLOXLogger.info(group=MLOXLogger.RULES, event=MLOXLogger.VALIDATED, 
                report="Rule successfully validated", terse="Order rule passed checks.")
```
✅ **Enforces structured logging with predefined values.**  
✅ **Prevents typos & ensures readability.**  

---

### **❌ Incorrect Example (Will Raise an Error)**
```python
MLOXLogger.info(group="Modding", event="okay", report="Rule check done")  # ❌ Typos
```
🚨 **Error: Invalid log group: Modding**  

---

## **4️⃣ Internals: How `MLOXLogger` Works**
```python
import logging

class MLOXLogger:
    """Centralized logging system for MLOXMaker with structured groups & events."""

    # Logging Groups
    RULES = "RULES"
    API = "API"
    FILE = "FILE"
    SYSTEM = "SYSTEM"

    # Logging Events
    STARTED = "STARTED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    VALIDATED = "VALIDATED"
    MISSING = "MISSING"

    # Logging Levels
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    LOGGER = logging.getLogger("MLOXMaker")

    @staticmethod
    def _log(*, group: str, event: str, report: str, terse: str | None = None, level: str = INFO):
        """Handles structured logging internally while enforcing valid groups & events."""
        if group not in {MLOXLogger.RULES, MLOXLogger.API, MLOXLogger.FILE, MLOXLogger.SYSTEM}:
            raise ValueError(f"Invalid log group: {group}")
        if event not in {MLOXLogger.STARTED, MLOXLogger.COMPLETED, MLOXLogger.FAILED, MLOXLogger.VALIDATED, MLOXLogger.MISSING}:
            raise ValueError(f"Invalid log event: {event}")

        formatted_message = f"{report} → {terse}" if terse else report
        getattr(MLOXLogger.LOGGER, level.lower())(formatted_message, extra={"tag": group, "event": event})

    @staticmethod
    def debug(*args, **kwargs):
        MLOXLogger._log(level=MLOXLogger.DEBUG, *args, **kwargs)

    @staticmethod
    def info(*args, **kwargs):
        MLOXLogger._log(level=MLOXLogger.INFO, *args, **kwargs)

    @staticmethod
    def warning(*args, **kwargs):
        MLOXLogger._log(level=MLOXLogger.WARNING, *args, **kwargs)

    @staticmethod
    def error(*args, **kwargs):
        MLOXLogger._log(level=MLOXLogger.ERROR, *args, **kwargs)

    @staticmethod
    def critical(*args, **kwargs):
        MLOXLogger._log(level=MLOXLogger.CRITICAL, *args, **kwargs)
```
✅ **Prevents invalid log messages.**  
✅ **Ensures log entries are categorized properly.**  

---

## **5️⃣ Advanced Logging Features**
### **🔹 Dynamic Log Level Configuration**
You can change the logging level at runtime:
```python
MLOXLogger.LOGGER.setLevel(logging.WARNING)
```
✅ Adjusts logging **without restarting**.  

### **🔹 Enabling or Disabling Logging Outputs**
```python
MLOXLogger.LOGGER.handlers.clear()  # Disables logging output
```
✅ **Gives control over log outputs.**  

---

## **6️⃣ Future Extensions**
- **New Log Groups** → Add categories like `EXPORT`, `IMPORT` as features expand.  
- **New Log Events** → More detailed tracking (e.g., `RETRY`, `IGNORED`).  
- **Performance Monitoring** → Log execution times for optimizations.  

---

## **7️⃣ Conclusion**
MLOXMaker’s logging system provides:
- **Structured, categorized logging**
- **Consistent debugging & error tracking**
- **Extendability for future features**

Because **good logging is a form of documentation**. 🚀🔥  

---

[Table of contents](index.md)
