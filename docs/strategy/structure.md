[Table of contents](index.md)

# Project Structure
The following provides simple guidelines to help keep the project organized. They are polite suggestions not hard rules.
```
MLOXMaker/
├── src/
│   ├── mloxmaker/                # Main application package
│   │   ├── __init__.py
│   │   ├── models/              # Data structures & ORM models
│   │   │   ├── __init__.py
│   │   │   ├── rule.py          # Rule model (e.g. [Order], [Conflict], [Requires])
│   │   │   └── mod.py           # Mod metadata and relationships
│   │   ├── views/               # PySide6 UI components
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py   # Dashboard & navigation
│   │   │   ├── rule_editor.py   # Create/Edit rule interface
│   │   │   ├── mod_analyzer.py  # Interface for analyzing mod dependencies/conflicts
│   │   │   └── visualization.py # Graph & table views of mod relationships
│   │   ├── controllers/         # Business logic (MVC controllers)
│   │   │   ├── __init__.py
│   │   │   ├── rule_controller.py  # Handles rule creation, editing, export
│   │   │   └── mod_controller.py   # Manages Nexus API lookups and mod analysis
│   │   ├── services/            # External services integration
│   │   │   ├── __init__.py
│   │   │   └── nexus_api.py     # Nexus Mods API integration, including caching via requests-cache
│   │   ├── database/            # SQLite and SQLAlchemy integration
│   │   │   ├── __init__.py
│   │   │   ├── db.py            # Database session, engine, and models initialization
│   │   │   └── migrations/      # Future-proof for schema changes (e.g. Alembic scripts)
│   │   ├── config/              # App settings & configuration
│   │   │   ├── __init__.py
│   │   │   └── settings.py      # Config variables (API keys, file paths, etc.)
│   │   └── utils/               # Helper functions and common utilities
│   │       ├── __init__.py
│   │       └── helpers.py
│   ├── assets/                  # Non-code assets
│   │   ├── images/              # Icons, logos, and UI graphics (including wireframes)
│   │   │   ├── icons/
│   │   │   └── wireframes/
│   ├── tests/                   # Unit and integration tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_controllers.py
│   │   └── test_services.py
│   └── main.py                  # Entry point for the desktop application
├── requirements.txt             # Python dependencies (e.g., PySide6, SQLAlchemy, networkx)
├── setup.py or pyproject.toml   # Packaging configuration for distribution & PyInstaller
├── README.md                    # Project overview and usage instructions
└── .gitignore                   # Git ignore file (e.g., __pycache__, .env, build artifacts)
```

### Key Points of This Structure

- **Separation of Concerns:**  
  - **Models, Views, and Controllers:**  
    - _Models_ are isolated under `models/` to handle data (e.g., mlox rules and mod metadata).  
    - _Views_ (using PySide6) are kept in `views/` to manage all UI components, aligned with your wireframes and UI design
    - _Controllers_ contain the business logic that bridges your models and views, ensuring clear MVC separation
  
- **Services & Integration:**  
  - The `services/` directory encapsulates integrations like the Nexus Mods API, which not only aids in dependency and conflict detection but also improves maintainability by isolating external communication logic.
  
- **Database Management:**  
  - The `database/` folder keeps SQLite and SQLAlchemy interactions organized and prepared for future migrations
  
- **Testing & Packaging:**  
  - A dedicated `tests/` folder for unit tests (using pytest) and integration tests separately.  
  - Packaging and distribution files (like `setup.py` or `pyproject.toml`) and a proper `.gitignore` file support clean project management and distribution (via PyInstaller).

---

[Table of contents](index.md)
