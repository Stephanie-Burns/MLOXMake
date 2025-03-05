
from MLOXMaker.database.manager import DatabaseManager
from MLOXMaker.database.models import Rule, Mod, Dependency


def test_add_and_get_rule(test_db):
    """Test adding and retrieving a rule."""
    DatabaseManager.add_rule("Order", "TestMod.esp", "AnotherMod.esp", "High", "Test note")

    rules = DatabaseManager.get_rules()
    assert len(rules) == 1
    assert rules[0].mod_name == "TestMod.esp"
    assert rules[0].target_mod == "AnotherMod.esp"
    assert rules[0].severity == "High"


def test_add_and_get_mod(test_db):
    """Test adding and retrieving a mod."""
    DatabaseManager.add_mod("CoolMod.esp", "hash123", "Nexus")

    mods = DatabaseManager.get_mods()
    assert len(mods) == 1
    assert mods[0].mod_name == "CoolMod.esp"
    assert mods[0].mod_hash == "hash123"
    assert mods[0].source == "Nexus"


def test_add_and_get_dependency(test_db):
    """Test adding and retrieving a mod dependency."""
    mod1 = Mod(mod_name="Master.esp")
    mod2 = Mod(mod_name="Addon.esp")

    test_db.add_all([mod1, mod2])
    test_db.commit()

    DatabaseManager.add_dependency(mod1.id, mod2.id)

    dependencies = DatabaseManager.get_dependencies()
    assert len(dependencies) == 1
    assert dependencies[0].mod_id == mod1.id
    assert dependencies[0].depends_on == mod2.id


def test_update_rule(test_db):
    """Test updating a rule."""
    DatabaseManager.add_rule("Conflict", "X.esp", "Y.esp", "High", "Initial note")

    rule = test_db.query(Rule).filter_by(mod_name="X.esp").first()
    assert rule is not None

    rule.severity = "Low"
    test_db.commit()

    updated_rule = test_db.query(Rule).filter_by(mod_name="X.esp").first()
    assert updated_rule.severity == "Low"


def test_delete_mod(test_db):
    """Test deleting a mod."""
    DatabaseManager.add_mod("RemoveMe.esp")

    mod = test_db.query(Mod).filter_by(mod_name="RemoveMe.esp").first()
    assert mod is not None

    test_db.delete(mod)
    test_db.commit()

    deleted_mod = test_db.query(Mod).filter_by(mod_name="RemoveMe.esp").first()
    assert deleted_mod is None
