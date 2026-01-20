import os
import shlex
import json
# go build -o bpls.exe BPLS.go To run: ./bpls.exe
# clear screen
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
clear()

class BPLS_Interpreter:
    def __init__(self):
        self.objects = {}     # object names (or None if not in a group)
        self.groups = {}      # group names
        self.variables = {}   # variable names

    def substitute(self, token):
        # Resolve variable if it exists
        return self.variables.get(token, token)

    def run(self, query: str):
        tokens = shlex.split(query.strip())
        if not tokens:
            return "Error: Empty command."

        cmd = tokens[0].upper()

        # VARIABLE "varname" IS "name"
        if cmd == "VARIABLE" and len(tokens) >= 4 and tokens[2].upper() == "IS":
            varname = tokens[1].strip('"')
            value = tokens[3].strip('"')
            self.variables[varname] = value
            return f"Variable '{varname}' is set to '{value}'."

        # CREATE OBJ <name>
        elif cmd == "CREATE" and len(tokens) >= 3 and tokens[1].upper() == "OBJ":
            obj_name = tokens[2]
            self.objects[obj_name] = None
            return f"Object '{obj_name}' created."

        # CREATE GROUP <name>
        elif cmd == "CREATE" and len(tokens) >= 3 and tokens[1].upper() == "GROUP":
            group_name = tokens[2]
            self.groups[group_name] = []
            return f"Group '{group_name}' created."

        # Clear screen cmd
        elif cmd == "CLEAR":
            clear()
            return ""

        # LOC <obj>
        elif cmd == "LOC" and len(tokens) >= 2:
            obj_name = self.substitute(tokens[1])
            if obj_name not in self.objects:
                return f"Error: Object '{obj_name}' not found."
            group = self.objects[obj_name]
            if group:
                index = self.groups[group].index(obj_name) + 1
                return f"Object '{obj_name}' is located in group '{group}' at ITEM {index}."
            else:
                return f"Object '{obj_name}' is not in any group."

        # FIND ITEM <n> OF <group>
        elif cmd == "FIND" and len(tokens) >= 5 and tokens[1].upper() == "ITEM" and tokens[3].upper() == "OF":
            try:
                n = int(tokens[2])
            except ValueError:
                return "Error: ITEM number must be an integer."
            group_name = self.substitute(tokens[4])
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            group = self.groups[group_name]
            if n <= 0 or n > len(group):
                return f"Error: Group '{group_name}' does not have ITEM {n}."
            return f"Group '{group_name}' ITEM {n} is '{group[n-1]}'"

        # SUM <group>
        elif cmd == "SUM" and len(tokens) >= 2:
            group_name = self.substitute(tokens[1])
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            ints = [int(x) for x in self.groups[group_name] if str(x).isdigit()]
            if not ints:
                return f"No Integers in ({group_name})"
            return f"SUM of '{group_name}' = {sum(ints)}"

        # AVG <group>
        elif cmd == "AVG" and len(tokens) >= 2:
            group_name = self.substitute(tokens[1])
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            ints = [int(x) for x in self.groups[group_name] if str(x).isdigit()]
            if not ints:
                return f"No Integers in ({group_name})"
            return f"AVG of '{group_name}' = {sum(ints)/len(ints)}"

        # SWAP <word> WITH <otherword> IN <group>
        elif cmd == "SWAP":
            upper_tokens = [t.upper() for t in tokens]
            if "WITH" in upper_tokens and "IN" in upper_tokens:
				# place holder 
                with_index = upper_tokens.index("WITH")
                in_index = upper_tokens.index("IN")
                word = tokens[1]
                otherword = tokens[with_index + 1]
                group_name = self.substitute(tokens[in_index + 1])
                if group_name not in self.groups:
                    return f"Error: Group '{group_name}' not found."
                self.groups[group_name] = [
                    otherword if x == word else x for x in self.groups[group_name]
                ]
                return f"Swapped '{word}' with '{otherword}' in group '{group_name}'."

        # DELETE OBJ <name>
        elif cmd == "DELETE" and len(tokens) >= 3 and tokens[1].upper() == "OBJ":
            obj_name = self.substitute(tokens[2])
            if obj_name not in self.objects:
                return f"Error: Object '{obj_name}' not found."
            group = self.objects[obj_name]
            if group and obj_name in self.groups[group]:
                self.groups[group].remove(obj_name)
            del self.objects[obj_name]
            return f"Object '{obj_name}' deleted."

        # DELETE GROUP <name>
        elif cmd == "DELETE" and len(tokens) >= 3 and tokens[1].upper() == "GROUP":
            group_name = self.substitute(tokens[2])
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            for obj in self.groups[group_name]:
                self.objects[obj] = None
            del self.groups[group_name]
            return f"Group '{group_name}' deleted."

        # SAVE CODE TO <filename>
        elif cmd == "SAVE" and len(tokens) >= 4 and tokens[1].upper() == "CODE" and tokens[2].upper() == "TO":
            filename = tokens[3]
            snapshot = {"objects": self.objects, "groups": self.groups, "variables": self.variables}
            with open(filename, "w") as f:
                json.dump(snapshot, f)
            return f"Code saved to '{filename}'."

        # LOAD <filename>
        elif cmd == "LOAD" and len(tokens) >= 2:
            filename = tokens[1]
            if not os.path.exists(filename):
                return f"Error: File '{filename}' not found."
            with open(filename, "r") as f:
                snapshot = json.load(f)
            self.objects = snapshot.get("objects", {})
            self.groups = snapshot.get("groups", {})
            self.variables = snapshot.get("variables", {})
            return f"Code loaded from '{filename}'."

        # MAKE FILE <file_name>
        elif cmd == "MAKE" and len(tokens) >= 3 and tokens[1].upper() == "FILE":
            filename = tokens[2].strip('"')
            with open(filename, "w"):
                pass
            return f"File '{filename}' created."

        # MAKE FOLDER <folder_name>
        elif cmd == "MAKE" and len(tokens) >= 3 and tokens[1].upper() == "FOLDER":
            foldername = tokens[2].strip('"')
            try:
                os.makedirs(foldername, exist_ok=True)
                return f"Folder '{foldername}' created."
            except Exception as e:
                return f"Error creating folder '{foldername}': {e}"

        # MOVE FILE <file_name> TO <folder_name>
        elif cmd == "MOVE" and len(tokens) >= 5 and tokens[1].upper() == "FILE" and tokens[3].upper() == "TO":
            filename = tokens[2].strip('"')
            foldername = tokens[4].strip('"')
            if not os.path.exists(filename):
                return f"Error: File '{filename}' not found."
				# place holder
            if not os.path.exists(foldername):
                return f"Error: Folder '{foldername}' not found."
            try:
                new_path = os.path.join(foldername, os.path.basename(filename))
                os.rename(filename, new_path)
                return f"File '{filename}' moved to folder '{foldername}'."
            except Exception as e:
                return f"Error moving file: {e}"

        # PUT "group_name" IN "file_name"
        elif cmd == "PUT" and len(tokens) >= 4 and tokens[2].upper() == "IN":
            group_name = self.substitute(tokens[1].strip('"'))
            filename = tokens[3].strip('"')
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            try:
                with open(filename, "w") as f:
                    for obj in self.groups[group_name]:
                        f.write(obj + "\n")
                return f"Group '{group_name}' written into file '{filename}'."
            except Exception as e:
                return f"Error writing group '{group_name}' to file '{filename}': {e}"

        # MOVE VARIABLE <varname> TO <group>
		# place holder
        elif cmd == "MOVE" and len(tokens) >= 5 and tokens[1].upper() == "VARIABLE" and tokens[3].upper() == "TO":
            varname = tokens[2].strip('"')
            if varname not in self.variables:
                return f"Error: Variable '{varname}' not found."
            obj_name = self.variables[varname]
            group_name = tokens[4].strip('"')
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            if obj_name not in self.objects:
                return f"Error: Object '{obj_name}' not found."
            old_group = self.objects[obj_name]
            if old_group and obj_name in self.groups[old_group]:
                self.groups[old_group].remove(obj_name)
            self.groups[group_name].append(obj_name)
            self.objects[obj_name] = group_name
            return f"Object '{obj_name}' (from variable '{varname}') moved to group '{group_name}'."

        # REMOVE OBJ "objname" FROM "groupname"
        elif cmd == "REMOVE" and len(tokens) >= 5 and tokens[1].upper() == "OBJ" and tokens[3].upper() == "FROM":
            obj_name = tokens[2].strip('"')
            group_name = tokens[4].strip('"')
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            if obj_name not in self.groups[group_name]:
                return f"Error: Object '{obj_name}' not in group '{group_name}'."
            self.groups[group_name].remove(obj_name)
            self.objects[obj_name] = None
            return f"Object '{obj_name}' removed from group '{group_name}'."

        # FIND OBJ "objname" FROM "groupname"
        elif cmd == "FIND" and len(tokens) >= 5 and tokens[1].upper() == "OBJ" and tokens[3].upper() == "FROM":
            obj_name = tokens[2].strip('"')
            group_name = tokens[4].strip('"')
            if group_name not in self.groups:
                return f"Error: Group '{group_name}' not found."
            if obj_name in self.groups[group_name]:
                return f"Object '{obj_name}' found in group '{group_name}'."
            else:
                return f"Object '{obj_name}' not found in group '{group_name}'."

        else:
            return "Error: Unknown command."


# Initialize interpreter once
interpreter = BPLS_Interpreter()

# Input loop
while True:
    try:
        cmd = input("BPLS> ")
        if cmd.strip().upper() in ["EXIT", "QUIT"]:
            print("Exiting BPLS interpreter.")
            break
        output = interpreter.run(cmd)
        print(output)
    except KeyboardInterrupt:
        print("\nExiting BPLS interpreter.")
        break
