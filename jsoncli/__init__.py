import argparse
import json

def get_value(obj, key_path):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    for key in keys:
        if key.isdigit():
            key = int(key)
        try:
            obj = obj[key]
        except (KeyError, IndexError):
            return None
    return obj

def set_value(obj, key_path, value):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    current = obj
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        if key not in current:
            current[key] = {} if keys[keys.index(key) + 1].isdigit() else {}
        current = current[key]
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
    current[last_key] = value

def add_value(obj, key_path, value):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    current = obj
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        if key not in current:
            current[key] = {} if keys[keys.index(key) + 1].isdigit() else {}
        current = current[key]
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
    if last_key in current:
        raise ValueError(f"Key '{last_key}' already exists.")
    current[last_key] = value

def delete_value(obj, key_path):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    current = obj
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        if key not in current:
            raise ValueError(f"Key '{key}' does not exist.")
        current = current[key]
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
    if last_key not in current:
        raise ValueError(f"Key '{last_key}' does not exist.")
    del current[last_key]

def validate_json(json_str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False
    
def main():
    parser = argparse.ArgumentParser(description="Command-line utility for manipulating JSON files.")
    parser.add_argument("command", choices=["get", "set", "add", "delete", "validate"], help="Specify the command")
    parser.add_argument("file", help="Path to the JSON file")
    parser.add_argument("key_path", nargs="?", help="Dot or slash separated key path for get, set, and add commands")
    parser.add_argument("value", nargs="?", help="Value for set and add commands")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        data = json.load(f)

    if args.command == "get":
        key_path = args.key_path
        value = get_value(data, key_path)
        print(value)
    elif args.command == "set":
        key_path = args.key_path
        value = json.loads(args.value)
        set_value(data, key_path, value)
        with open(args.file, "w") as f:
            json.dump(data, f, indent=2)
    elif args.command == "add":
        key_path = args.key_path
        value = json.loads(args.value)
        add_value(data, key_path, value)
        with open(args.file, "w") as f:
            json.dump(data, f, indent=2)
    elif args.command == "delete":
        key_path = args.key_path
        delete_value(data, key_path)
        with open(args.file, "w") as f:
            json.dump(data, f, indent=2)
    elif args.command == "validate":
        with open(args.file, "r") as f:
            json_str = f.read()
        if validate_json(json_str):
            print("Valid JSON.")
        else:
            print("Invalid JSON.")
     
if __name__ == "__main__":
    main()