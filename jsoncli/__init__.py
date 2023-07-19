import argparse
import json
import os

def get_value(data, keys):
    for key in keys:
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list):
            try:
                key = int(key)
                data = data[key]
            except (IndexError, ValueError):
                data = None
        else:
            return None
        if data is None:
            break
    return data

def set_value(data, keys, value):
    for key in keys[:-1]:
        if isinstance(data, dict):
            data = data.setdefault(key, {})
        elif isinstance(data, list):
            try:
                key = int(key)
            except ValueError:
                return False
            if key >= len(data):
                data.extend([{}] * (key - len(data) + 1))
            data = data[key]
        else:
            return False
    if isinstance(data, dict):
        data[keys[-1]] = value
    elif isinstance(data, list):
        try:
            keys[-1] = int(keys[-1])
            data[keys[-1]] = value
        except ValueError:
            return False
    else:
        return False
    return True

def add_value(data, keys, value):
    for key in keys[:-1]:
        if isinstance(data, dict):
            data = data.setdefault(key, {})
        elif isinstance(data, list):
            try:
                key = int(key)
            except ValueError:
                return False
            if key >= len(data):
                data.extend([{}] * (key - len(data) + 1))
            data = data[key]
        else:
            return False
    if keys[-1] not in data:
        if isinstance(data, dict):
            data[keys[-1]] = value
        elif isinstance(data, list):
            try:
                keys[-1] = int(keys[-1])
                data[keys[-1]] = value
            except ValueError:
                return False
        else:
            return False
        return True
    return False


def delete_value(data, keys):
    for key in keys[:-1]:
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list):
            try:
                key = int(key)
                data = data[key]
            except (IndexError, ValueError):
                return False
        else:
            return False
        if data is None:
            return False
    if isinstance(data, dict):
        return keys[-1] in data and data.pop(keys[-1], None) is not None
    elif isinstance(data, list):
        try:
            keys[-1] = int(keys[-1])
            if keys[-1] < len(data):
                data.pop(keys[-1])
                return True
        except ValueError:
            return False
    return False

def main():
    parser = argparse.ArgumentParser(description="⚡ Manipulate JSON files through CLI ⚡")
    parser.add_argument("command", choices=["get", "set", "add", "delete"], help="Command to perform")
    parser.add_argument("file", help="JSON file to manipulate")
    parser.add_argument("keys", nargs="*", help="Keys to target the value")
    parser.add_argument("--value", help="Value to set or add")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"File '{args.file}' not found.")
        return

    with open(args.file, "r") as json_file:
        data = json.load(json_file)

    if args.command == "get":
        value = get_value(data, args.keys)
        if value is not None:
            print(value)
        else:
            print("Value not found")
    elif args.command == "set":
        if args.value is None:
            print("Please provide a value to set")
        else:
            if set_value(data, args.keys, args.value):
                with open(args.file, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                print("Value set successfully")
            else:
                print("Error setting value")
    elif args.command == "add":
        if args.value is None:
            print("Please provide a value to add")
        else:
            if add_value(data, args.keys, args.value):
                with open(args.file, "w") as json_file:
                    json.dump(data, json_file, indent=4)
                print("Value added successfully")
            else:
                print("Error adding value")
    elif args.command == "delete":
        if delete_value(data, args.keys):
            with open(args.file, "w") as json_file:
                json.dump(data, json_file, indent=4)
            print("Value deleted successfully")
        else:
            print("Error deleting value")
            
if __name__ == "__main__":
    main()