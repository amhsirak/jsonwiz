import argparse
import json

__version__ = "0.0.1"


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


def set_value(obj, key_path, value, data_type=None):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    current = obj
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        if isinstance(current, list):
            if key >= len(current):
                current.extend([{}] * (key - len(current) + 1))
            current = current[key]
        elif key not in current:
            current[key] = {} if keys[keys.index(key) + 1].isdigit() else {}
            current = current[key]
        else:
            current = current[key]

    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)

    if isinstance(current, list) and data_type=="list":
        if last_key >= len(current):
            current.extend([{}] * (last_key - len(current) + 1))
        current[last_key] = convert_to_data_type(value, data_type)
    else:
        current[last_key] = convert_to_data_type(value, data_type)


def delete_value(obj, key_path):
    keys = key_path.split('.') if '.' in key_path else key_path.split('/')
    current = obj
    for key in keys[:-1]:
        if key.isdigit():
            key = int(key)
        if isinstance(current, list):
            if key < 0 or key >= len(current):
                raise ValueError(f"Index '{key}' is out of range.")
        elif key not in current:
            raise ValueError(f"Key '{key}' does not exist.")
        current = current[key]
    last_key = keys[-1]
    if last_key.isdigit():
        last_key = int(last_key)
    if isinstance(current, list):
        if last_key < 0 or last_key >= len(current):
            raise ValueError(f"Index '{last_key}' is out of range.")
    elif last_key not in current:
        raise ValueError(f"Key '{last_key}' does not exist.")
    if isinstance(current, list):
        current.pop(last_key)
    else:
        del current[last_key]


def validate_json(json_str):
    try:
        json.loads(json_str)
        return True
    except ValueError:
        return False


def convert_to_data_type(value, data_type):
    if data_type == "string":
        return str(value)
    elif data_type == "integer":
        return int(value)
    elif data_type == "float":
        return float(value)
    elif data_type == "boolean":
        return bool(value)
    elif data_type == "null":
        return None
    elif data_type == "object":
        return json.loads(value)
    elif data_type == "list":
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            # If the value is not a valid JSON list, convert it to a list containing the value as a string
            return [value]
    else:
        return value


def main():
    parser = argparse.ArgumentParser(
        description="⚡ JSONCLI - A command line interface for manipulating JSON files ⚡")
    parser.add_argument("command", choices=[
                        "get", "set", "delete", "validate"], help="Specify the command to run")
    parser.add_argument("file", help="Path to the JSON file")
    parser.add_argument("key_path", nargs="?",
                        help="Dot or slash separated key path for get, set, and add commands")
    parser.add_argument("value", nargs="?",
                        help="Value for set and add commands")
    parser.add_argument("--type", choices=["string", "integer", "float", "boolean",
                        "null", "object", "list"], help="Specify the data type of the new value")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        data = json.load(f)

    if args.command == "get":
        key_path = args.key_path
        value = get_value(data, key_path)
        print(value)
    elif args.command == "set":
        key_path = args.key_path
        value = args.value
        data_type = args.type
        set_value(data, key_path, value, data_type)
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
