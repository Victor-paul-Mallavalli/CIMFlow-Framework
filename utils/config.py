import json

def load_arch_config(path="arch_config.json"):
    with open(path) as f:
        return json.load(f)
