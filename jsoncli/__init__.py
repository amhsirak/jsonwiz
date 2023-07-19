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

def main():
    parser = argparse.ArgumentParser(description="⚡ Manipulate JSON files through CLI ⚡")
    parser.add_argument("command", choices=["get"], help="Command to perform")
    parser.add_argument("file", help="JSON file to manipulate")
    parser.add_argument("keys", nargs="*", help="Keys to target the value")
    parser.add_argument("--value", help="Value to set or add")
    args = parser.parse_args()
            
if __name__ == "__main__":
    main()