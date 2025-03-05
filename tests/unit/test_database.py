from MLOXMaker.database.models import Rule, Mod, Dependency


def test_create_rule(test_db):
    """Test inserting a rule into the database."""
    rule = Rule(rule_type="Order", mod_name="A.esp", target_mod="B.esp", severity="Medium")
    test_db.add(rule)
    test_db.commit()

    retrieved = test_db.query(Rule).filter_by(mod_name="A.esp").first()
    assert retrieved is not None
    assert retrieved.target_mod == "B.esp"

def test_create_mod(test_db):
    """Test inserting a mod into the database."""
    mod = Mod(mod_name="CoolMod.esp", mod_hash="abc123", source="Nexus")
    test_db.add(mod)
    test_db.commit()

    retrieved = test_db.query(Mod).filter_by(mod_name="CoolMod.esp").first()
    assert retrieved is not None
    assert retrieved.mod_hash == "abc123"

def test_create_dependency(test_db):
    """Test inserting a mod dependency."""
    mod1 = Mod(mod_name="Master.esp")
    mod2 = Mod(mod_name="Addon.esp")
    test_db.add_all([mod1, mod2])
    test_db.commit()

    dep = Dependency(mod_id=mod1.id, depends_on=mod2.id)
    test_db.add(dep)
    test_db.commit()

    retrieved = test_db.query(Dependency).filter_by(mod_id=mod1.id).first()
    assert retrieved is not None
    assert retrieved.depends_on == mod2.id

def test_update_rule(test_db):
    """Test updating a rule."""
    rule = Rule(rule_type="Conflict", mod_name="X.esp", target_mod="Y.esp", severity="High")
    test_db.add(rule)
    test_db.commit()

    rule.severity = "Low"
    test_db.commit()

    retrieved = test_db.query(Rule).filter_by(mod_name="X.esp").first()
    assert retrieved.severity == "Low"

def test_delete_mod(test_db):
    """Test deleting a mod."""
    mod = Mod(mod_name="RemoveMe.esp")
    test_db.add(mod)
    test_db.commit()

    test_db.delete(mod)
    test_db.commit()

    retrieved = test_db.query(Mod).filter_by(mod_name="RemoveMe.esp").first()
    assert retrieved is None
