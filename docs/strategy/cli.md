[Table of contents](index.md)

---

### **📌 CLI Mode Plan for MLOXMaker** 🚀  
 


---

## **1️⃣ Overview**
MLOXMaker’s **CLI mode** provides a lightweight, scriptable interface for **validating rules, checking mod conflicts, and managing rule sets**—without launching the GUI.  

*👋 Say Hi to the cli!*

✅ **Why include it?**  
- **Fast rule validation** without opening the full app.  
- **Automation & scripting** (integrate into modding workflows).  
- **Useful for power users** who prefer the command line.  

---

## **2️⃣ CLI Features & Commands**  

### **🔹 Rule Validation**
```bash
mloxmaker validate some_rule.txt
```
📌 **Checks for syntax errors, missing mods, and logical contradictions.**  
📌 **Outputs results** in a clean, readable format.  

---

### **🔹 Check Mod Dependencies**
```bash
mloxmaker dependencies SomeMod.esp
```
📌 Lists **dependencies required** by `SomeMod.esp`.  
📌 Pulls from **both user-defined rules & Nexus API (if available).**  

---

### **🔹 Check Mod Conflicts**
```bash
mloxmaker conflicts SomeMod.esp
```
📌 Scans for **conflicting mods** based on **existing rules**.  
📌 Suggests **possible fixes** (e.g., reordering, exclusions).  

---

### **🔹 Export Rules**
```bash
mloxmaker export --format txt
```
📌 Saves the rules as `mlox_user.txt`.  
📌 Other formats (`--format json`) for structured output.  

---

### **🔹 Interactive Mode (Optional)**
```bash
mloxmaker shell
```
📌 Opens an **interactive prompt** (`>>>`) for rule queries.  
📌 Example usage:  
```bash
>>> validate "some_rule.txt"
>>> check dependencies "SomeMod.esp"
>>> exit
```
📌 **Great for debugging & quick lookups!**  

---

## **3️⃣ CLI Output & Logging**
🔹 **User-Friendly Output:**  
```
[✔] Rule valid: No errors found.
[⚠] Warning: Missing dependency "SomeRequiredMod.esp".
[❌] Conflict detected: "ModA.esp" vs "ModB.esp".
```
🔹 **Optional `--verbose` flag** for detailed logging.  
🔹 **Exit codes:**  
- `0` = Success ✅  
- `1` = Warnings ⚠  
- `2` = Errors ❌  

---

## **4️⃣ Implementation Details**
🔹 CLI will be **a separate module (`cli.py`)**, integrating with the **main rule system**.  
🔹 Uses **Argparse** for parsing commands.  
🔹 **Unit tests** to cover command-line behavior.  

---

## **5️⃣ Summary**
✅ **Minimal, scriptable interface** for quick rule validation.  
✅ **Useful commands for rule checks, dependencies, and conflicts.**  
✅ **Automation-friendly** (works in scripts, modding pipelines).  
✅ **Expandable in the future** (could integrate with a web version).  

---

[Table of contents](index.md)
