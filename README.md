
# BPLS — Beginner Programming Language for Statistics

## TL;DR

**Purpose**  
BPLS (Beginner Programming Language for Statistics) is a lightweight, beginner-oriented programming language designed for basic statistical calculations, object and group management, and simple file operations through an interactive interpreter.

**Capabilities**
- Variable handling  
- Object and group creation  
- Basic statistical functions (`SUM`, `AVG`)  
- Object searching, modification, and deletion  
- File and folder management  
- Saving and loading program state  

**Legal Notice**  
BPLS is provided **"as is"**, without warranty of any kind, express or implied.  
The authors and contributors assume no liability for any damages, losses, or issues arising from the use of this software. Use is entirely at your own risk.

---

## Overview
BPLS is a beginner-friendly programming language focused on simple statistical operations and structured data management.

🚧 **Project Status: Beta**
- Bugs are expected  
- Features may change or be incomplete  
- Feedback is appreciated  

If you find bugs, have feedback, or ideas for new features, please report them in the  
[Issues](https://github.com/LemonsandLimez/BPLS/issues) section.

---

## File Variants

### Python
- Requires Python **3.6+** (Recommended: 3.9+)  
- Size: ~12 KB  
- Best option if Python is already installed

### Go
- Requires Go **1.10+** (Recommended: 1.18+)  
- Size: ~12 KB  
- Faster than Python if Go is pre-installed

### Windows Executable (.exe)
- Windows 7+  
- Size: ~3.26 MB  
- Does not require Python or Go  
- Heaviest option, but easiest for users without dependencies

---

## Installation

### Windows
1. Download `BPLS.exe` from Releases  
2. Run from File Explorer or terminal:
```bash
./BPLS.exe
```

### Python
Ensure Python 3.6+ is installed, then run:
```bash
python BPLS.py
```

### Go
Ensure Go 1.10+ is installed, then run:
```bash
go run BPLS.go
```

---

## BPLS Interpreter Command Guide

### Variable Management
```
VARIABLE "varname" IS "value"
```

### Object and Group Creation
```
CREATE OBJ <name>
CREATE GROUP <name>
```

### Screen Control
```
CLEAR
```

### Object Location and Search
```
LOC <obj>
FIND ITEM <n> OF <group>
FIND OBJ "objname" FROM "groupname"
```

### Math Operations
```
SUM <group>
AVG <group>
```

### Modification Commands
```
SWAP <word> WITH <otherword> IN <group>
REMOVE OBJ "objname" FROM "groupname"
MOVE VARIABLE <varname> TO <group>
```

### Deletion
```
DELETE OBJ <name>
DELETE GROUP <name>
```

### Saving and Loading
```
SAVE CODE TO "filename"
LOAD <filename>
```

### File and Folder Management
```
MAKE FILE "file_name"
MAKE FOLDER "folder_name"
MOVE FILE <file_name> TO <folder_name>
PUT "group_name" IN "file_name"
```

### Exit Commands
```
EXIT
QUIT
```

---

## Quick Start Example

### Code
```
CREATE GROUP stats
CREATE OBJ x
VARIABLE "num" IS 42
MOVE VARIABLE num TO stats
SUM stats
```

### Expected Output
```
SUM of stats = 42
```

---

## Contributing
BPLS is in **Beta**. Contributions are welcome.

- Report bugs or suggest features via the Issues section  
- Submit pull requests for improvements or fixes  

---

## Legal Disclaimer
BPLS is provided **"as is"**, without warranty of any kind, express or implied.  
The authors and contributors are not responsible for any damages, losses, or issues that may arise from using this software. By using BPLS, you agree that you do so at your own risk.
