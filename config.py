import json
from arcade import color
from map.hexagonal import Hex
from draw import make_hexagon_texture


def jsonread(path):
    with open(path) as json_file:
        return json.load(json_file)


MAP_HEX_RADIUS = 30
MAP_HEX_OUTLINE_WIDTH = 5
MAP_HEX_OUTLINE_COLOR = "#918585"

ENTITIES_CONFIG_PATH = "game_configs/units_config.json"
FRACTIONS_CONFIG_PATH = "game_configs/fractions_config.json"

ENTITIES_CONFIG = jsonread(ENTITIES_CONFIG_PATH)
FRACTIONS_CONFIG = jsonread(FRACTIONS_CONFIG_PATH)

TREE_ID = ENTITIES_CONFIG["tree"]["entity_id"]
OWNED_TILE_ID = ENTITIES_CONFIG["ownedtile"]["entity_id"]
OWNED_TILE_HP_CLASS = ENTITIES_CONFIG["ownedtile"]["health"]
OWNED_TILE_SALARY = ENTITIES_CONFIG["ownedtile"]["salary"]

COLORS = {
    "GREEN": color.GREEN_YELLOW,
    "RED": (199, 21, 133),
    "BLUE": color.CAMBRIDGE_BLUE,
    "COLUMBIA_BLUE": color.COLUMBIA_BLUE,
    "BLUEGRAY": color.BLUE_GRAY
}

ENTITY_ID2COST = dict()
for entity in ENTITIES_CONFIG.keys():
    ENTITY_ID2COST.update({
        ENTITIES_CONFIG[entity]["entity_id"] : ENTITIES_CONFIG[entity]["cost"]
    })



class Assets:
    def __init__(self):
        self.entities_textures = {}

        for key in ENTITIES_CONFIG.keys():
            try:
                self.entities_textures.update(
                    { ENTITIES_CONFIG[key]["entity_id"] : ENTITIES_CONFIG[key]["texture"] }
                )
            except KeyError:
                pass

        self.hex_textures = {}

    def add_hexagon_textures(self):
        zero_hex = Hex()
        zero_hex.init(MAP_HEX_RADIUS, shiftx=0, shifty=50, fill_color=color.GREEN_YELLOW, outline_width=MAP_HEX_OUTLINE_WIDTH)

        TEXTURES = COLORS.keys()
        self.hex_textures = {}

        for T in TEXTURES:
            self.hex_textures.update( {
                T : make_hexagon_texture(MAP_HEX_RADIUS, COLORS[T],
                                              zero_hex.cpoints, MAP_HEX_OUTLINE_COLOR, MAP_HEX_OUTLINE_WIDTH)
            })


ASSETS = Assets()
ASSETS.add_hexagon_textures()