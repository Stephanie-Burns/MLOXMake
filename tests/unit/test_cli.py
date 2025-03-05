import sys
from contextlib import redirect_stdout
from io import StringIO

from MLOXMaker.cli import cli_main
from MLOXMaker.database.manager import DatabaseManager


def run_cli_command(command):
    """Helper to mock CLI execution and capture output."""
    sys.argv = ["mloxmaker"] + command.split()
    output = StringIO()
    with redirect_stdout(output):  # ✅ Ensure stdout is correctly redirected
        cli_main()
    return output.getvalue().strip()

def test_validate_empty_db():
    """Test validate command when no rules exist."""
    output = run_cli_command("validate")
    assert "No rules found." in output

def test_list_mods_empty_db():
    """Test list-mods command when no mods exist."""
    output = run_cli_command("list-mods")
    assert "No mods found." in output

def test_validate_with_rules():
    """Test validate command when rules exist."""
    DatabaseManager.add_rule("Order", "TestMod.esp", "AnotherMod.esp", "High")
    output = run_cli_command("validate")
    assert "✅ 1 rules loaded." in output
    assert "📌 Order: TestMod.esp -> AnotherMod.esp" in output

def test_list_mods_with_data():
    """Test list-mods command when mods exist."""
    DatabaseManager.add_mod("CoolMod.esp", "hash123", "Nexus")
    output = run_cli_command("list-mods")
    assert "📦 1 mods installed." in output
    assert "📜 CoolMod.esp (Source: Nexus)" in output
