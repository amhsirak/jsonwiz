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