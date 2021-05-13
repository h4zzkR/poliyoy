from config import ASSETS


class GameState(object):
    """
    Синглтон с разными нужными вещами
    """
    last_mouse_tile_pos = (-1, -1)
    last_mouse_right_tile_pos = (-1, -1)
    last_mouse_tile_texture = ASSETS.hex_textures["GREEN"]
    last_fraction_id = None
    bot_id = 0

    changed_tiles = dict() # для изменения цвета выбранных клеток
    fractions = dict()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GameState, cls).__new__(cls)
        return cls.instance

    def set_pos(self, col, row):
        self.last_mouse_tile_pos = (col, row)

    def set_right_pos(self, col, row):
        self.last_mouse_right_tile_pos = (col, row)

    def set_texture(self, texture):
        self.last_mouse_tile_texture = texture

    def set_fraction(self, fraction_id):
        self.last_fraction = fraction_id

    def append_fraction(self, fraction):
        self.fractions.update({fraction.fraction_id : fraction})

    def set_fractions(self, fractions: list):
        self.fractions = dict()
        for fraction in fractions:
            self.fractions.update({fraction.fraction_id: fraction})
            if fraction.isBot:
                self.bot_id = fraction.fraction_id

    def append_to_tiles(self, pos, texture):
        self.changed_tiles.update({pos : texture})

    def get_last_fraction(self):
        return self.fractions[self.last_fraction]

    def get_bot_fraction(self):
        return self.fractions[self.bot_id]