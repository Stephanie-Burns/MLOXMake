## **✅ What the mlox Visualization & Rule Automation Tool Should Do**  

### **Rule Creation & Editing**  
- Provide an **easy way to create mlox rules** without manual writing.  
- Support **structured rule creation** (e.g., `[Order]`, `[Conflict]`, `[Requires]` via forms or guided input).  
- Allow **manual rule editing** with **syntax highlighting** for the mlox DSL.  
- Offer **auto-suggestions** for mod names, dependencies, and rule components.  
- Ensure **rules are properly formatted** to prevent syntax errors.  

### **Dependency & Conflict Management**  
- Integrate with **Nexus Mods API** to:  
  - Search for mods by **name, ID, MD5 hash**.  
  - Pull **dependency and conflict data** automatically.  
  - Suggest **missing dependencies** for a given mod.  
- Help users **discover conflicts** by cross-referencing Nexus data and existing mlox rules.  


### **Visualization & Usability**  
- Offer a **visual representation** of mod relationships (dependencies & conflicts).  
- Allow **drag-and-drop or structured input** for managing rules.  
- Support **different views** for mod relationships:  
  - **Graph/tree-based** (mod dependencies visualized).  
  - **Table format** (structured rules list).  

### **Rule Management & Exporting**  
- Allow users to **save & load custom rule sets** for personal use.  
- Support **exporting rules** in a format compatible with mlox (`mlox_user.txt`).  
- Keep a **history of changes** so users can undo/redo edits.  

### **Future-Proofing & Expansion**  
- Work **offline**, only requiring internet for Nexus Mods API lookups.  
- Stay **separate from mlox’s core function** (assists with rule creation, doesn’t sort load orders).  
- Potentially **sync with mlox’s GitHub rules repository** to keep rules up to date.  
- Allow for **future migration to a web-based system** if adoption grows.  



## **❌ What It Should NOT Do**  

### **Avoid Overlapping with mlox**  
- **Not a load order sorter** – mlox handles that. This tool **only helps create rules**.  
- **Not a mod manager** – doesn’t install, enable, or disable mods (leave that to MO2, Wrye Mash, etc.).  
- **Not an automatic fixer** – suggests fixes but doesn’t apply them automatically.  

### **Avoid Overcomplicating Things**  
- **No complex coding knowledge required** – users shouldn’t need to learn mlox DSL by heart.  
- **No unnecessary manual data entry** – fetch as much info as possible from Nexus API.  
- **No required internet connection** – should function offline, except for online features.  
