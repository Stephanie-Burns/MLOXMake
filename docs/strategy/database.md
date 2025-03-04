
[Table of contents](index.md)

---

## **📌 MLOXMaker Database Design Document**  

### **1️⃣ Overview**
MLOXMaker uses **SQLite** to store mod rules, dependencies, and metadata.  
- **Why SQLite?** → **Structured, fast querying, and ideal for graph-based rule visualization.**  
- **Schema Stability** → The database will be **finalized before release** to avoid user-facing migrations.  
- **Settings Storage** → **Remains in JSON** for transparency.  

---

### **2️⃣ Database Location**  
- **Default Path**: `~/.config/mloxmaker/mloxmaker.db`  
- **Portable Mode**: If applicable, allow user-defined database location.  

---

### **3️⃣ Database Schema**
📌 **Tables:**
1️⃣ **`rules`** → Stores **mlox rules** (`[Order]`, `[Conflict]`, etc.).  
2️⃣ **`mods`** → Stores **mod metadata** (names, hashes, dependencies).  
3️⃣ **`dependencies`** → Stores **mod-to-mod dependency relationships**.  

---

#### **📝 `rules` Table (Mod Load Order & Conflict Rules)**
Stores all user-defined and auto-generated **mlox rules**.

| Column Name    | Type        | Description |
|---------------|------------|-------------|
| `id`          | INTEGER (PK) | Unique ID for each rule |
| `rule_type`   | TEXT (NOT NULL) | Type of rule (`Order`, `Conflict`, `Requires`) |
| `mod_name`    | TEXT (NOT NULL) | Affected mod |
| `target_mod`  | TEXT | The mod being referenced (e.g., required/conflicted mod) |
| `severity`    | TEXT | Optional (`Low`, `Medium`, `High`) for conflicts |
| `notes`       | TEXT | User-defined notes on rule |
| `created_at`  | TIMESTAMP DEFAULT CURRENT_TIMESTAMP | Rule creation date |

📌 **Indexes:**  
- `(mod_name, rule_type, target_mod)` → **Fast lookup for rules affecting a mod**.  

---

#### **📝 `mods` Table (Mod Metadata)**
Stores **installed or referenced mods**.

| Column Name   | Type        | Description |
|--------------|------------|-------------|
| `id`         | INTEGER (PK) | Unique ID for each mod |
| `mod_name`   | TEXT (NOT NULL) | Name of the mod |
| `mod_hash`   | TEXT (UNIQUE) | Unique mod hash (optional) |
| `source`     | TEXT | `Local` (installed) or `Nexus` (fetched) |
| `last_updated` | TIMESTAMP | Last modification time |

📌 **Indexes:**  
- `mod_hash` → **Ensures unique mod tracking**.  

---

#### **📝 `dependencies` Table (Mod Relationships)**
Stores **mod-to-mod dependencies**.

| Column Name   | Type        | Description |
|--------------|------------|-------------|
| `id`         | INTEGER (PK) | Unique ID for each dependency |
| `mod_id`     | INTEGER (FK to `mods.id`) | Mod that has a dependency |
| `depends_on` | INTEGER (FK to `mods.id`) | Required mod |

📌 **Indexes:**  
- `(mod_id, depends_on)` → **Fast lookup for dependencies**.  

---

### **4️⃣ Query Examples**
🔍 **Get all rules affecting a mod**:
```sql
SELECT rule_type, target_mod, severity 
FROM rules WHERE mod_name = 'SomeMod.esp';
```

🔍 **Find all dependencies for a mod**:
```sql
SELECT m2.mod_name AS required_mod 
FROM dependencies 
JOIN mods m1 ON dependencies.mod_id = m1.id 
JOIN mods m2 ON dependencies.depends_on = m2.id 
WHERE m1.mod_name = 'SomeMod.esp';
```

---

### **5️⃣ Schema Evolution & Migrations**
- **Migrations (Alembic) used only during development.**  
- **Final schema locked before production.**  
- **Future schema updates (if needed)** handled via a **one-time upgrade script**.  

---

### **6️⃣ Summary**
✅ **SQLite for structured rule storage**  
✅ **JSON for user settings**  
✅ **No user-facing migrations**  
✅ **Schema designed for fast querying & visualization**  

---

[Table of contents](index.md)
