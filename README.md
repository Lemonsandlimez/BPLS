#### TL;DR

### Purpose
BPLS (Beginner Programming Language for Statistics) is a lightweight, beginner-oriented programming language for basic statistical calculations, object and group management, and simple file operations through an interactive interpreter.

### Capabilities
BPLS supports variable handling, object and group creation, basic statistical functions (such as SUM and AVG), object searching and modification, file and folder management, and saving/loading program state.

### Legal Notice
BPLS is provided **"as is"**, without warranty of any kind, express or implied.  
The authors and contributors assume no liability for any damages, losses, or issues arising from the use of this software. Use is entirely at your own risk.


# BPLS — Beginner Programming Language for Statistics

## Overview
**BPLS** is a beginner-friendly programming language designed for basic statistical operations and simple object and group management.

This project is currently in **Beta**. Features may change, break, or be incomplete.  
If you find bugs, have feedback, or ideas for new features, please report them in the **Issues** section.

---

## Legal Disclaimer
BPLS is provided **"as is"**, without warranty of any kind, express or implied.  
The authors and contributors are not responsible for any damages, losses, or issues that may arise from using this software.

By using BPLS, you agree that you do so **at your own risk**.

---

## Project Status
🚧 **Beta Version**
- Bugs are expected
- Features may change or be incomplete
- Feedback is appreciated

---

## File Variants

### Python File
- Python **3.6 or higher** (Recommended: Python 3.9+)
- File size: ~12 KB
- Best if Python is already installed

### GoLang File
- Go **1.10 or higher** (Recommended: Go 1.18+)
- File size: ~12 KB
- Faster than Python if Go is pre-installed

### Windows Executable (.exe)
- Windows 7 or higher
- File size: ~3.26 MB
- Does not require Python or Go
- **Not recommended** unless dependencies cannot be installed

---

## BPLS Interpreter Command Guide

The BPLS Interpreter provides commands to manage variables, objects, groups, and interact with the file system.

---

### Variable Management
VARIABLE "varname" IS "value"

Defines a variable and assigns it a value for later use.

---

### Object and Group Creation
CREATE OBJ
CREATE GROUP

- Creates a new object
- Creates a new group (container for objects)

---

### Screen Control
CLEAR

Clears the terminal screen.

---

### Object Location and Search
LOC
FIND ITEM OF
FIND OBJ "objname" FROM "groupname"

- Shows where an object is located
- Retrieves the nth item from a group
- Checks if an object exists inside a group

---

### Math Operations
SUM
AVG

- Adds all integer values in a group
- Calculates the average of integer values in a group

---

### Modification Commands
SWAP WITH IN
REMOVE OBJ "objname" FROM "groupname"
MOVE VARIABLE TO

- Replaces one word with another inside a group
- Removes an object from a group
- Moves the object referenced by a variable into a group

---

### Deletion
DELETE OBJ
DELETE GROUP

- Deletes an object completely
- Deletes a group and detaches all objects inside it

---

### Saving and Loading
SAVE CODE TO "filename"
LOAD

- Saves the current state (objects, groups, variables) to a JSON file
- Loads a previously saved state

---

### File and Folder Management
MAKE FILE "file_name"
MAKE FOLDER "folder_name"
MOVE FILE <file_name> TO <folder_name>
PUT "group_name" IN "file_name"

- Creates files and folders
- Moves files into folders
- Writes the contents of a group into a file

---

### Exit Commands
EXIT
QUIT

Ends the interpreter session.
