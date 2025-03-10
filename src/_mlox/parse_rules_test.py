from _mlox.mlox_parser import rule_parser

RULE_FILE = "mlox_base.txt"

class NameConverter:
    """A dummy name converter that returns names unchanged."""
    def cname(self, name):
        return name

    def truename(self, name):
        return name

def load_and_print_rules():
    """Loads rules from `mlox_base.txt` and prints them."""
    parser = rule_parser(plugin_list=[], datadir=None, name_converter=NameConverter())  # ✅ Fix applied!
    success = parser.read_rules(RULE_FILE)

    if success:
        print("✅ Rules loaded successfully!\n")
        print(parser.get_messages())  # 🔥 Print parsed rule messages
    else:
        print("❌ Failed to parse rules.")

if __name__ == "__main__":
    load_and_print_rules()
