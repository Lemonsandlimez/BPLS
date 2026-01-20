# BPLS is in Beta, if you find any bugs; Please go to the issues sectoin. Please give feedback, or ideas for new additoins in the issues section
This is BPLS, Beginners Programing Language for Statistics
# File Varients:
# Python File (versoin 3.6 or higher)* (Recomended: Python 3.9+)
Around 12KB, Best if you have Python Pre-Installed
# GoLang File (versoin 1.10 or higher)* (Recomended: Go 1.18+)
Around 12KB, better than Python if Pre-Installed (because it is faster)
# .exe File (Windows Exucutable, Windows 7+) (No recomendatoin)
Around 3.26MB, heaviest of them all, doesnt require Python / Go installatoin though, which can be heavier (Many GB of RAM)

# BPLS Interpreter Command Guide

The BPLS Interpreter provides commands to manage objects, groups, variables, and interact with the file system.

---

# Variable Management
- VARIABLE "varname" IS "name"
  Defines a variable and assigns it a value for later use.

---

# Object and Group Creation
- CREATE OBJ <name>
  Creates a new object.
- CREATE GROUP <name>
  Creates a new group (container for objects).

# Screen Control
- CLEAR
  Clears the terminal screen.

# Object Location and Search
- LOC <obj>
  Shows where an object is located (group and position).
- FIND ITEM <n> OF <group>
  Retrieves the nth item from a group.
- FIND OBJ "objname" FROM "groupname"
  Checks if an object exists inside a group.

# Math Operations
- SUM <group>
  Adds all integer values in a group.
- AVG <group>
  Calculates the average of integer values in a group.

# Modification Commands
- SWAP <word> WITH <otherword> IN <group>
  Replaces one word with another inside a group.
- REMOVE OBJ "objname" FROM "groupname"
  Removes an object from a group.
- MOVE VARIABLE <varname> TO <group>
  Moves the object referenced by a variable into a group.

# Deletion
- DELETE OBJ <name>
  Deletes an object completely.
- DELETE GROUP <name>
  Deletes a group and detaches all objects inside it.

# Saving and Loading
- SAVE CODE TO "filename"
  Saves the current state (objects, groups, variables) into a JSON file.
LOAD <filename>
  Loads a previously saved state from a JSON file.
# File and Folder Management
- MAKE FILE "file_name"
  Creates a new empty file.
- MAKE FOLDER "folder_name"
  Creates a new folder.
- MOVE FILE <file_name> TO <folder_name>
  Moves a file into a folder.
- PUT "group_name" IN "file_name"
  Writes the contents of a group into a file.


# Exit
- EXIT / QUIT
  Ends the interpreter session.
