
from MLOXMaker.database.db import SessionLocal, engine, Base
from MLOXMaker.database.models import Rule, Mod, Dependency

class DatabaseManager:
    """Manages database interactions for MLOXMaker."""

    @staticmethod
    def get_session():
        """Returns a new database session."""
        return SessionLocal()

    @staticmethod
    def initialize():
        """Ensures all tables are created before using the database."""
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def add_rule(rule_type, mod_name, target_mod=None, severity=None, notes=None):
        """Adds a new rule to the database."""
        with DatabaseManager.get_session() as session:
            rule = Rule(rule_type=rule_type, mod_name=mod_name, target_mod=target_mod, severity=severity, notes=notes)
            session.add(rule)
            session.commit()

    @staticmethod
    def get_rules():
        """Retrieves all rules from the database."""
        with DatabaseManager.get_session() as session:
            return session.query(Rule).all()

    @staticmethod
    def add_mod(mod_name, mod_hash=None, source=None):
        """Adds a new mod to the database."""
        with DatabaseManager.get_session() as session:
            mod = Mod(mod_name=mod_name, mod_hash=mod_hash, source=source)
            session.add(mod)
            session.commit()

    @staticmethod
    def get_mods():
        """Retrieves all mods from the database."""
        with DatabaseManager.get_session() as session:
            return session.query(Mod).all()

    @staticmethod
    def add_dependency(mod_id, depends_on_id):
        """Adds a dependency between two mods."""
        with DatabaseManager.get_session() as session:
            dep = Dependency(mod_id=mod_id, depends_on=depends_on_id)
            session.add(dep)
            session.commit()

    @staticmethod
    def get_dependencies():
        """Retrieves all dependencies."""
        with DatabaseManager.get_session() as session:
            return session.query(Dependency).all()
