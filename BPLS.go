package main

// cd "C:\Users\antho\Programing Projects"; go build -o bpls.exe BPLS.go; .\bpls.exe
import (
	"bufio"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"
)

func clear() {
	cmd := exec.Command("clear") // Linux / Mac
	if os.Getenv("OS") == "Windows_NT" {
		cmd = exec.Command("cmd", "/c", "cls")
	}
	cmd.Stdout = os.Stdout
	cmd.Run()
}

type BPLSInterpreter struct {
	objects   map[string]string
	groups    map[string][]string
	variables map[string]string
	queue     []string
}

func NewBPLSInterpreter() *BPLSInterpreter {
	return &BPLSInterpreter{
		objects:   make(map[string]string),
		groups:    make(map[string][]string),
		variables: make(map[string]string),
		queue:     []string{},
	}
}

func (b *BPLSInterpreter) substitute(token string) string {
	if val, ok := b.variables[token]; ok {
		return val
	}
	return token
}

func indexOf(slice []string, val string) int {
	for i, v := range slice {
		if v == val {
			return i
		}
	}
	return -1
}

func contains(slice []string, val string) bool {
	for _, v := range slice {
		if v == val {
			return true
		}
	}
	return false
}

func removeFromSlice(slice []string, val string) []string {
	result := []string{}
	for _, v := range slice {
		if v != val {
			result = append(result, v)
		}
	}
	return result
}

func splitArgs(input string) []string {
	var args []string
	var current strings.Builder
	inQuotes := false
	for _, r := range input {
		switch r {
		case ' ':
			if inQuotes {
				current.WriteRune(r)
			} else if current.Len() > 0 {
				args = append(args, current.String())
				current.Reset()
			}
		case '"':
			inQuotes = !inQuotes
		default:
			current.WriteRune(r)
		}
	}
	if current.Len() > 0 {
		args = append(args, current.String())
	}
	return args
}

func (b *BPLSInterpreter) Run(input string) string {
	tokens := splitArgs(input)
	if len(tokens) == 0 {
		return "Error: Empty command."
	}

	cmd := strings.ToUpper(tokens[0])

	switch cmd {
	case "VARIABLE":
		if len(tokens) >= 4 && strings.ToUpper(tokens[2]) == "IS" {
			varName := strings.Trim(tokens[1], `"`)
			value := strings.Trim(tokens[3], `"`)
			b.variables[varName] = value
			return fmt.Sprintf("Variable '%s' set to '%s'.", varName, value)
		}

	case "CREATE":
		if len(tokens) >= 3 {
			switch strings.ToUpper(tokens[1]) {
			case "OBJ":
				objName := strings.Trim(tokens[2], `"`)
				b.objects[objName] = ""
				return fmt.Sprintf("Object '%s' created.", objName)
			case "GROUP":
				groupName := strings.Trim(tokens[2], `"`)
				b.groups[groupName] = []string{}
				return fmt.Sprintf("Group '%s' created.", groupName)
			}
		}

	case "CLEAR":
		clear()
		return ""

	case "LOC":
		if len(tokens) >= 2 {
			obj := b.substitute(tokens[1])
			group, ok := b.objects[obj]
			if !ok {
				return fmt.Sprintf("Error: Object '%s' not found.", obj)
			}
			if group == "" {
				return fmt.Sprintf("Object '%s' is not in any group.", obj)
			}
			idx := indexOf(b.groups[group], obj)
			return fmt.Sprintf("Object '%s' is located in group '%s' at ITEM %d.", obj, group, idx+1)
		}

	case "FIND":
		if len(tokens) >= 5 && strings.ToUpper(tokens[1]) == "ITEM" && strings.ToUpper(tokens[3]) == "OF" {
			n, err := strconv.Atoi(tokens[2])
			if err != nil {
				return "Error: ITEM number must be an integer."
			}
			group := b.substitute(tokens[4])
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			if n <= 0 || n > len(list) {
				return fmt.Sprintf("Error: Group '%s' does not have ITEM %d.", group, n)
			}
			return fmt.Sprintf("Group '%s' ITEM %d is '%s'.", group, n, list[n-1])
		}

	case "SUM":
		if len(tokens) >= 2 {
			group := b.substitute(tokens[1])
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			sum := 0
			count := 0
			for _, v := range list {
				if n, err := strconv.Atoi(v); err == nil {
					sum += n
					count++
				}
			}
			if count == 0 {
				return fmt.Sprintf("No integers in group '%s'.", group)
			}
			return fmt.Sprintf("SUM of '%s' = %d", group, sum)
		}

	case "AVG":
		if len(tokens) >= 2 {
			group := b.substitute(tokens[1])
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			sum := 0
			count := 0
			for _, v := range list {
				if n, err := strconv.Atoi(v); err == nil {
					sum += n
					count++
				}
			}
			if count == 0 {
				return fmt.Sprintf("No integers in group '%s'.", group)
			}
			return fmt.Sprintf("AVG of '%s' = %f", group, float64(sum)/float64(count))
		}

	case "SWAP":
		upperTokens := make([]string, len(tokens))
		for i, t := range tokens {
			upperTokens[i] = strings.ToUpper(t)
		}
		if contains(upperTokens, "WITH") && contains(upperTokens, "IN") {
			withIdx := indexOf(upperTokens, "WITH")
			inIdx := indexOf(upperTokens, "IN")
			if withIdx < 1 || inIdx <= withIdx {
				return "Error: Invalid SWAP syntax."
			}
			obj1 := tokens[1]
			obj2 := tokens[withIdx+1]
			group := b.substitute(tokens[inIdx+1])
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			for i, v := range list {
				if v == obj1 {
					list[i] = obj2
				} else if v == obj2 {
					list[i] = obj1
				}
			}
			b.groups[group] = list
			return fmt.Sprintf("Swapped '%s' with '%s' in group '%s'.", obj1, obj2, group)
		}

	case "MOVE":
		if len(tokens) >= 5 && strings.ToUpper(tokens[1]) == "VARIABLE" && strings.ToUpper(tokens[3]) == "TO" {
			varName := strings.Trim(tokens[2], `"`)
			objName, ok := b.variables[varName]
			if !ok {
				return fmt.Sprintf("Error: Variable '%s' not found.", varName)
			}
			group := strings.Trim(tokens[4], `"`)
			if _, ok := b.groups[group]; !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			if _, ok := b.objects[objName]; !ok {
				return fmt.Sprintf("Error: Object '%s' not found.", objName)
			}
			oldGroup := b.objects[objName]
			if oldGroup != "" {
				b.groups[oldGroup] = removeFromSlice(b.groups[oldGroup], objName)
			}
			b.groups[group] = append(b.groups[group], objName)
			b.objects[objName] = group
			return fmt.Sprintf("Object '%s' (from variable '%s') moved to group '%s'.", objName, varName, group)
		}
		if len(tokens) >= 3 && strings.ToUpper(tokens[2]) == "TO" {
			objName := strings.Trim(tokens[1], `"`)
			group := strings.Trim(tokens[3], `"`)
			if _, ok := b.groups[group]; !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			if _, ok := b.objects[objName]; !ok {
				return fmt.Sprintf("Error: Object '%s' not found.", objName)
			}
			oldGroup := b.objects[objName]
			if oldGroup != "" {
				b.groups[oldGroup] = removeFromSlice(b.groups[oldGroup], objName)
			}
			b.groups[group] = append(b.groups[group], objName)
			b.objects[objName] = group
			return fmt.Sprintf("Object '%s' moved to group '%s'.", objName, group)
		}

	case "REMOVE":
		if len(tokens) >= 5 && strings.ToUpper(tokens[1]) == "OBJ" && strings.ToUpper(tokens[3]) == "FROM" {
			objName := strings.Trim(tokens[2], `"`)
			group := strings.Trim(tokens[4], `"`)
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			if !contains(list, objName) {
				return fmt.Sprintf("Error: Object '%s' not in group '%s'.", objName, group)
			}
			b.groups[group] = removeFromSlice(list, objName)
			b.objects[objName] = ""
			return fmt.Sprintf("Object '%s' removed from group '%s'.", objName, group)
		}

	case "LIST":
		if len(tokens) >= 2 {
			group := b.substitute(tokens[1])
			list, ok := b.groups[group]
			if !ok {
				return fmt.Sprintf("Error: Group '%s' not found.", group)
			}
			if len(list) == 0 {
				return fmt.Sprintf("Group '%s' is empty.", group)
			}
			return fmt.Sprintf("Group '%s': %s", group, strings.Join(list, ", "))
		}

	case "SAVE":
		if len(tokens) >= 4 && strings.ToUpper(tokens[1]) == "CODE" && strings.ToUpper(tokens[2]) == "TO" {
			filename := tokens[3]
			f, err := os.Create(filename)
			if err != nil {
				return fmt.Sprintf("Error creating file '%s': %v", filename, err)
			}
			defer f.Close()
			data := map[string]interface{}{
				"objects":   b.objects,
				"groups":    b.groups,
				"variables": b.variables,
			}
			enc := json.NewEncoder(f)
			if err := enc.Encode(data); err != nil {
				return fmt.Sprintf("Error encoding JSON: %v", err)
			}
			return fmt.Sprintf("Code saved to '%s'.", filename)
		}

	case "LOAD":
		if len(tokens) >= 2 {
			filename := tokens[1]
			f, err := os.Open(filename)
			if err != nil {
				return fmt.Sprintf("Error opening file '%s': %v", filename, err)
			}
			defer f.Close()
			var data map[string]interface{}
			dec := json.NewDecoder(f)
			if err := dec.Decode(&data); err != nil {
				return fmt.Sprintf("Error decoding JSON: %v", err)
			}
			if objs, ok := data["objects"].(map[string]interface{}); ok {
				b.objects = make(map[string]string)
				for k, v := range objs {
					b.objects[k] = v.(string)
				}
			}
			if grps, ok := data["groups"].(map[string]interface{}); ok {
				b.groups = make(map[string][]string)
				for k, v := range grps {
					arr := []string{}
					if slice, ok := v.([]interface{}); ok {
						for _, s := range slice {
							arr = append(arr, s.(string))
						}
					}
					b.groups[k] = arr
				}
			}
			if vars, ok := data["variables"].(map[string]interface{}); ok {
				b.variables = make(map[string]string)
				for k, v := range vars {
					b.variables[k] = v.(string)
				}
			}
			return fmt.Sprintf("Code loaded from '%s'.", filename)
		}
	}

	return "Error: Command not recognized or incomplete."
}

func main() {
	clear()
	interpreter := NewBPLSInterpreter()
	scanner := bufio.NewScanner(os.Stdin)

	fmt.Println("BPLS v1.3 - Beginner’s Programming Language for Statistics")
	fmt.Println("Type commands to queue them. Use RUN CODE to execute all queued commands.")
	fmt.Println("Type EXIT or QUIT to leave.\n")

	for {
		fmt.Print("BPLS> ")
		if !scanner.Scan() {
			fmt.Println("\nExiting BPLS interpreter.")
			break
		}
		cmd := scanner.Text()
		upperCmd := strings.ToUpper(strings.TrimSpace(cmd))

		if upperCmd == "EXIT" || upperCmd == "QUIT" {
			fmt.Println("Exiting BPLS interpreter.")
			break
		}

		if upperCmd == "RUN CODE" {
			start := time.Now()
			fmt.Printf("START: %v\n", start.Format("15:04:05"))

			for _, line := range interpreter.queue {
				output := interpreter.Run(line)
				if output != "" {
					fmt.Println(output)
				}
			}

			end := time.Now()
			diff := end.Sub(start)
			fmt.Printf("END:   %v\n", end.Format("15:04:05"))
			fmt.Printf("DURATION: %v\n", diff)

			interpreter.queue = []string{} // clear queue
		} else {
			interpreter.queue = append(interpreter.queue, cmd)
		}
	}
}