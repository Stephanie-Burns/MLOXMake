[Table of contents](index.md)

## **📌 Main UI Screens**  

### **1️⃣ Home / Dashboard**
**Purpose:**  
- Acts as the **starting point** for users.  
- Quick access to major features: **Create Rule, Edit Rules, Analyze Mod, Visualize Rules, Export**.  
- Displays **recently modified rules** and **suggestions** (e.g., “You haven’t added dependencies for X mod”).  

**Components:**  
- **Navigation Bar** (Rule Editor, Visualization, Nexus Search, Export).  
- **Quick Actions** (Create New Rule, Analyze Mod, View Load Order).  
- **Recent Activity** (last edited rules, detected conflicts).  

---

### **2️⃣ Rule Editor (Create / Edit Rules)**
**Purpose:**  
- Provides a structured way to **create, edit, and validate mlox rules**.  

**Components:**  
- **Rule Type Selector** (`[Order]`, `[Conflict]`, `[Requires]`, etc.).  
- **Mod Search Field** (Installed mods / Nexus lookup).  
- **Structured Rule Input Fields** (Drag-drop, dropdowns, text fields).  
- **Preview Pane** (Live formatted rule output).  
- **Save / Validate Rule Buttons**.  

---

### **3️⃣ Mod Analyzer (Find Dependencies & Conflicts)**
**Purpose:**  
- Helps users **discover missing dependencies and conflicts** using Nexus Mods API & local rules.  

**Components:**  
- **Search Bar** (Find mod by name, ID, or hash).  
- **Mod Details Panel** (Metadata, dependencies, conflicts).  
- **Detected Issues Panel** (Missing dependencies, conflicts with installed mods).  
- **“Generate Rule” Button** (Auto-suggests rules).  

---

### **4️⃣ Rule Visualization**
**Purpose:**  
- Provides a **graphical way to understand mod relationships** (dependencies, conflicts, load order).  

**Components:**  
- **Graph View** (Mod connections shown visually).  
- **Table View** (Rules in a structured list).  
- **Interactive Elements** (Click a mod to see rules affecting it).  
- **Export Visualization Button** (Save or share view).  

---

### **5️⃣ Export & Settings**
**Purpose:**  
- Allows users to **save, load, and manage rulesets**.  

**Components:**  
- **Save to File** (`mlox_user.txt` for mlox compatibility).  
- **Load Rule Set** (Import previous rules).  
- **Export to JSON / Shareable Format** (For future web-based integration).  
- **Settings Panel** (Customization, offline mode, API keys if needed).  

---

[Table of contents](index.md)
