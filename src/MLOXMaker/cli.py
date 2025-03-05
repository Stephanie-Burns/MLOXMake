import argparse
from MLOXMaker.managers.app_log import AppLog, LogGroup, LogEvent
from MLOXMaker.database.manager import DatabaseManager


def validate_rules():
    """Validates stored rules and prints results."""
    rules = DatabaseManager.get_rules()
    if not rules:
        print("No rules found.")
        return

    print(f"✅ {len(rules)} rules loaded.")
    for rule in rules:
        print(f"📌 {rule.rule_type}: {rule.mod_name} -> {rule.target_mod or 'N/A'}")


def list_mods():
    """Lists all mods stored in the database."""
    mods = DatabaseManager.get_mods()
    if not mods:
        print("No mods found.")
        return

    print(f"📦 {len(mods)} mods installed.")
    for mod in mods:
        print(f"📜 {mod.mod_name} (Source: {mod.source or 'Unknown'})")


def cli_main():
    """CLI Entry Point"""
    parser = argparse.ArgumentParser(prog="mloxmaker", description="MLOXMaker CLI Tool")

    subparsers = parser.add_subparsers(dest="command")

    # 🛠️ Add CLI Commands
    subparsers.add_parser("validate", help="Validate stored rules")
    subparsers.add_parser("list-mods", help="List installed mods")

    args = parser.parse_args()

    if args.command == "validate":
        validate_rules()
    elif args.command == "list-mods":
        list_mods()
    else:
        parser.print_help()
