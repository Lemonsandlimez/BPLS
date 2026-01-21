# BPLS — Beginner Programming Language for Statistics

## TL;DR
**BPLS** is a lightweight, beginner-friendly programming language designed for simple statistical calculations, structured data management, and basic file operations through an interactive interpreter.

🚧 **Project Status: Beta**
- Bugs are expected
- Features may change
- Feedback is welcome

---

## Purpose
BPLS (Beginner Programming Language for Statistics) is built for newcomers to programming who want an easy way to work with numbers, groups, and basic statistics without complex syntax.

---

## Key Capabilities
- Variable handling
- Object and group creation
- Basic statistical functions (`SUM`, `AVG`)
- Object searching, modification, and deletion
- File and folder management
- Saving and loading program state

---

## File Variants

### GoLang (Recommended)
- Requires **GoLang 1.11+** (1.18+ recommended)
- Size: ~12 KB
- Best option if Go is already installed

### Python
- Requires **Python 3.6+**
- Size ~16KB
- Slower than Go, and heavier
- (Not recomended unless python already installed)

### Windows Executable (.exe)
- Windows 7+
- Size: ~3.26 MB
- No dependencies required (If your on Windows)
- Heaviest option, but easiest for users without dependencies

---

## Installation

### Windows
1. Download `BPLS.exe` from the Releases page
2. Run via File Explorer or terminal:

`./BPLS.exe`


### Python
Ensure Python 3.6+ is installed, then run:
`python BPLS.py`


### Go
1. Ensure GoLang 1.11+ Is installed (1.18+ Recomended)
2. Open terminal and run:

`go run BPLS.go`

---

## BPLS Interpreter Command Guide

### Variable Management
`VARIABLE "varname" IS "value"`


### Object & Group Creation
'CREATE OBJ "name"`

`CREATE GROUP "name`

### Screen Control
`CLEAR`


### Object Location & Search
`LOC "obj"`

`FIND ITEM n" OF "group"`

`FIND OBJ "objname" FROM "groupname"`


### Math Operations
`SUM <group>`

`AVG <group>`


### Modification Commands
`SWAP "word" WITH "otherword" IN "group"`

`REMOVE OBJ "objname" FROM "groupname"`

`MOVE VARIABLE "varname" TO "group"`


### Deletion
`DELETE OBJ "name"'

`DELETE GROUP "name"`


### Saving & Loading
`SAVE CODE TO "filename"`

`LOAD "filename"`


### File & Folder Management
`MAKE FILE "file_name"`

`MAKE FOLDER "folder_name"`

`MOVE FILE <file_name> TO <folder_name>`

`PUT "group_name" IN "file_name"`


### Exit Commands
`EXIT`
`QUIT`


---

## Quick Start Example

### Code
`CREATE GROUP stats
CREATE OBJ x
VARIABLE "num" IS 42
MOVE VARIABLE num TO stats
SUM stats`


### Expected Output
`SUM of stats = 42`


---

## Contributing
BPLS is currently in **Beta**, and contributions are welcome.

- Report bugs or suggest features via the Issues section
- Submit pull requests for improvements or fixes

---

## Legal Disclaimer
BPLS is provided **"as is"**, without warranty of any kind, express or implied.  
The authors and contributors assume no responsibility for any damages, losses, or issues arising from the use of this software.  
By using BPLS, you agree that you do so **at your own risk**.
