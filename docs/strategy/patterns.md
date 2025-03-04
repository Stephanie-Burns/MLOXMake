[Table of contents](index.md)

## **🛠️ Design Patterns**

---

### **1️⃣ MVC (Model-View-Controller)**
💡 **Why?** Keeps **data (models)**, **business logic (controllers)**, and **UI (views)** separate.
- **Model** → Stores rule/mod data (SQLAlchemy).  
- **View** → Handles UI components (PySide).  
- **Controller** → Manages rule operations, mod interactions.

---

### **2️⃣ Singleton for Database Session**
💡 **Why?** We only need **one connection** to the database at a time.

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "sqlite:///mlox_tool.db"

engine = create_engine(DATABASE_URL)
SessionLocal = scoped_session(sessionmaker(bind=engine))
```
---

### **3️⃣ Factory Pattern for Rule Creation**
💡 **Why?** Different rule types (`[Order]`, `[Conflict]`, `[Requires]`) should have **a common interface**.

```python
class RuleFactory:
    @staticmethod
    def create_rule(rule_type, **kwargs):
        if rule_type == "Order":
            return OrderRule(**kwargs)
        elif rule_type == "Conflict":
            return ConflictRule(**kwargs)
        elif rule_type == "Requires":
            return RequiresRule(**kwargs)
        else:
            raise ValueError("Invalid rule type")
```
This allows **adding new rule types easily** without modifying core logic.

---

### **4️⃣ Observer Pattern for UI Updates**
💡 **Why?** If a rule is **edited in the database**, the UI should **update automatically**.

```python
class RuleObserver:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self):
        for callback in self.subscribers:
            callback()
```
This ensures **real-time updates** across UI components.

---

[Table of contents](index.md)
