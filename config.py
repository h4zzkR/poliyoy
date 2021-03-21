import json
from enum import Enum

def jsonread(path):
    with open(path) as json_file:
        return json.load(json_file)

ENTITIES_CONFIG_PATH = "game_configs/units_config.json"
ENTITIES_CONFIG = jsonread(ENTITIES_CONFIG_PATH)