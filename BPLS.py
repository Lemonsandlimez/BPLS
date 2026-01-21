import os
import json
import shlex
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class BPLSInterpreter:
    def __init__(self):
        self.objects = {}     # objects
        self.groups = {}      # groups
        self.variables = {}   # variables
        self.queue = []       # queued commands

    def substitute(self, token):
        return self.variables.get(token, token)

    def index_of(self, lst, val):
        try:
            return lst.index(val)
        except ValueError:
            return -1

    def remove_from_list(self, lst, val):
        return [x for x in lst if x != val]

    def split_args(self, input_str):
        return shlex.split(input_str)

    def run(self, input_str):
        tokens = self.split_args(input_str)
        if not tokens:
            return "Error: Empty command."

        cmd = tokens[0].upper()

        # VARIABLE "varname" IS "value"
        if cmd == "VARIABLE" and len(tokens) >= 4 and tokens[2].upper() == "IS":
            varname = tokens[1].strip('"')
            value = tokens[3].strip('"')
            self.variables[varname] = value
            return f"Variable '{varname}' set to '{value}'."

        # CREATE OBJ / GROUP
        elif cmd == "CREATE" and len(tokens) >= 3:
            if tokens[1].upper() == "OBJ":
                objname = tokens[2].strip('"')
                self.objects[objname] = ""
                return f"Object '{objname}' created."
            elif tokens[1].upper() == "GROUP":
                groupname = tokens[2].strip('"')
                self.groups[groupname] = []
                return f"Group '{groupname}' created."

        elif cmd == "CLEAR":
            clear()
            return ""

        # LOC
        elif cmd == "LOC" and len(tokens) >= 2:
            obj = self.substitute(tokens[1])
            if obj not in self.objects:
                return f"Error: Object '{obj}' not found."
            group = self.objects[obj]
            if group == "":
                return f"Object '{obj}' is not in any group."
            idx = self.index_of(self.groups[group], obj)
            return f"Object '{obj}' is located in group '{group}' at ITEM {idx+1}."

        # FIND ITEM
        elif cmd == "FIND" and len(tokens) >= 5 and tokens[1].upper() == "ITEM" and tokens[3].upper() == "OF":
            try:
                n = int(tokens[2])
            except ValueError:
                return "Error: ITEM number must be an integer."
            group = self.substitute(tokens[4])
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            lst = self.groups[group]
            if n <= 0 or n > len(lst):
                return f"Error: Group '{group}' does not have ITEM {n}."
            return f"Group '{group}' ITEM {n} is '{lst[n-1]}'."

        # SUM / AVG
        elif cmd == "SUM" and len(tokens) >= 2:
            group = self.substitute(tokens[1])
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            ints = [int(v) for v in self.groups[group] if v.isdigit()]
            if not ints:
                return f"No integers in group '{group}'."
            return f"SUM of '{group}' = {sum(ints)}"

        elif cmd == "AVG" and len(tokens) >= 2:
            group = self.substitute(tokens[1])
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            ints = [int(v) for v in self.groups[group] if v.isdigit()]
            if not ints:
                return f"No integers in group '{group}'."
            return f"AVG of '{group}' = {sum(ints)/len(ints)}"

        # SWAP
        elif cmd == "SWAP":
            if "WITH" in [t.upper() for t in tokens] and "IN" in [t.upper() for t in tokens]:
                with_idx = [t.upper() for t in tokens].index("WITH")
                in_idx = [t.upper() for t in tokens].index("IN")
                obj1 = tokens[1]
                obj2 = tokens[with_idx+1]
                group = self.substitute(tokens[in_idx+1])
                if group not in self.groups:
                    return f"Error: Group '{group}' not found."
                self.groups[group] = [obj2 if v == obj1 else obj1 if v == obj2 else v for v in self.groups[group]]
                return f"Swapped '{obj1}' with '{obj2}' in group '{group}'."

        # MOVE VARIABLE TO / MOVE OBJ TO
        elif cmd == "MOVE":
            if len(tokens) >= 5 and tokens[1].upper() == "VARIABLE" and tokens[3].upper() == "TO":
                varname = tokens[2].strip('"')
                if varname not in self.variables:
                    return f"Error: Variable '{varname}' not found."
                objname = self.variables[varname]
                group = tokens[4].strip('"')
                if group not in self.groups:
                    return f"Error: Group '{group}' not found."
                if objname not in self.objects:
                    return f"Error: Object '{objname}' not found."
                old_group = self.objects[objname]
                if old_group:
                    self.groups[old_group] = self.remove_from_list(self.groups[old_group], objname)
                self.groups[group].append(objname)
                self.objects[objname] = group
                return f"Object '{objname}' (from variable '{varname}') moved to group '{group}'."
            elif len(tokens) >= 4 and tokens[2].upper() == "TO":
                objname = tokens[1].strip('"')
                group = tokens[3].strip('"')
                if group not in self.groups:
                    return f"Error: Group '{group}' not found."
                if objname not in self.objects:
                    return f"Error: Object '{objname}' not found."
                old_group = self.objects[objname]
                if old_group:
                    self.groups[old_group] = self.remove_from_list(self.groups[old_group], objname)
                self.groups[group].append(objname)
                self.objects[objname] = group
                return f"Object '{objname}' moved to group '{group}'."

        # REMOVE OBJ FROM GROUP
        elif cmd == "REMOVE" and len(tokens) >= 5 and tokens[1].upper() == "OBJ" and tokens[3].upper() == "FROM":
            objname = tokens[2].strip('"')
            group = tokens[4].strip('"')
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            if objname not in self.groups[group]:
                return f"Error: Object '{objname}' not in group '{group}'."
            self.groups[group] = self.remove_from_list(self.groups[group], objname)
            self.objects[objname] = ""
            return f"Object '{objname}' removed from group '{group}'."

        # DELETE OBJ / GROUP
        elif cmd == "DELETE":
            if len(tokens) >= 3 and tokens[1].upper() == "OBJ":
                objname = tokens[2].strip('"')
                if objname not in self.objects:
                    return f"Error: Object '{objname}' not found."
                group = self.objects[objname]
                if group and objname in self.groups[group]:
                    self.groups[group] = self.remove_from_list(self.groups[group], objname)
                del self.objects[objname]
                return f"Object '{objname}' deleted."
            elif len(tokens) >= 3 and tokens[1].upper() == "GROUP":
                group = tokens[2].strip('"')
                if group not in self.groups:
                    return f"Error: Group '{group}' not found."
                for obj in self.groups[group]:
                    self.objects[obj] = ""
                del self.groups[group]
                return f"Group '{group}' deleted."

        # LIST
        elif cmd == "LIST" and len(tokens) >= 2:
            group = self.substitute(tokens[1])
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            lst = self.groups[group]
            if not lst:
                return f"Group '{group}' is empty."
            return f"Group '{group}': {', '.join(lst)}"

        # SAVE / LOAD
        elif cmd == "SAVE" and len(tokens) >= 4 and tokens[1].upper() == "CODE" and tokens[2].upper() == "TO":
            filename = tokens[3]
            snapshot = {"objects": self.objects, "groups": self.groups, "variables": self.variables}
            with open(filename, "w") as f:
                json.dump(snapshot, f)
            return f"Group '{group}': {', '.join(lst)}"

        # SAVE CODE TO <filename>
        elif cmd == "SAVE" and len(tokens) >= 4 and tokens[1].upper() == "CODE" and tokens[2].upper() == "TO":
            filename = tokens[3]
            snapshot = {"objects": self.objects, "groups": self.groups, "variables": self.variables}
            try:
                with open(filename, "w") as f:
                    json.dump(snapshot, f)
                return f"Code saved to '{filename}'."
            except Exception as e:
                return f"Error saving code: {e}"

        # LOAD <filename>
        elif cmd == "LOAD" and len(tokens) >= 2:
            filename = tokens[1]
            if not os.path.exists(filename):
                return f"Error: File '{filename}' not found."
            try:
                with open(filename, "r") as f:
                    snapshot = json.load(f)
                self.objects = snapshot.get("objects", {})
                self.groups = snapshot.get("groups", {})
                self.variables = snapshot.get("variables", {})
                return f"Code loaded from '{filename}'."
            except Exception as e:
                return f"Error loading code: {e}"

        # MAKE FILE <file_name>
        elif cmd == "MAKE" and len(tokens) >= 3 and tokens[1].upper() == "FILE":
            filename = tokens[2].strip('"')
            try:
                with open(filename, "w"):
                    pass
                return f"File '{filename}' created."
            except Exception as e:
                return f"Error creating file '{filename}': {e}"

        # MAKE FOLDER <folder_name>
        elif cmd == "MAKE" and len(tokens) >= 3 and tokens[1].upper() == "FOLDER":
            foldername = tokens[2].strip('"')
            try:
                os.makedirs(foldername, exist_ok=True)
                return f"Folder '{foldername}' created."
            except Exception as e:
                return f"Error creating folder '{foldername}': {e}"

        # PUT "group_name" IN "file_name"
        elif cmd == "PUT" and len(tokens) >= 4 and tokens[2].upper() == "IN":
            group = self.substitute(tokens[1].strip('"'))
            filename = tokens[3].strip('"')
            if group not in self.groups:
                return f"Error: Group '{group}' not found."
            try:
                with open(filename, "w") as f:
                    for obj in self.groups[group]:
                        f.write(obj + "\n")
                return f"Group '{group}' written into file '{filename}'."
            except Exception as e:
                return f"Error writing group '{group}' to file '{filename}': {e}"

        return "Error: Command not recognized or incomplete."


def main():
    clear()
    interpreter = BPLSInterpreter()
    print("BPLS v1.3 - Beginner’s Programming Language for Statistics")
    print("Type commands to queue them. Use RUN CODE to execute all queued commands.")
    print("Type EXIT or QUIT to leave.\n")

    while True:
        try:
            cmd = input("BPLS> ").strip()
            upper_cmd = cmd.upper()
            if upper_cmd in ["EXIT", "QUIT"]:
                print("Exiting BPLS interpreter.")
                break
            elif upper_cmd == "RUN CODE":
                start = time.time()
                print(f"START: {time.strftime('%H:%M:%S', time.localtime(start))}")
                for line in interpreter.queue:
                    output = interpreter.run(line)
                    if output:
                        print(output)
                end = time.time()
                print(f"END:   {time.strftime('%H:%M:%S', time.localtime(end))}")
                print(f"DURATION: {end - start:.2f} seconds")
                interpreter.queue = []
            else:
                interpreter.queue.append(cmd)
        except KeyboardInterrupt:
            print("\nExiting BPLS interpreter.")
            break


if __name__ == "__main__":
    main()
