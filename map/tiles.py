from arcade import Sprite, SpriteList
from .hexagonal import Hex
from abstract import AbstractEntity
from fractions import Fraction
from config import ASSETS, COLORS

class TileDecorator(Hex):
    """
    Декоратор объекта Hex
    """

    entity: AbstractEntity = None
    sprite_entity: Sprite = None

    def __init__(self, *args, **kwargs) -> None:
        super(TileDecorator, self).__init__(*args, **kwargs)

    def is_empty(self):
        return self.entity is None

    def get_sprite(self):
        return self.sprite_entity

    def set_entity(self, entity: AbstractEntity = None) -> None:
        self.entity = entity
        self.sprite_entity = Sprite(ASSETS.entities_textures[entity.entity_id], 0.5)
        self.sprite_entity.set_position(self.center_x, self.center_y)
        self.sprite_entity._points = None

    def set_tile_texture(self, texture_id):
        try:
            self.texture = ASSETS.hex_textures[texture_id]
        except KeyError:
            raise NotImplementedError


    def move(self, col, row):
        self.entity.move_to((col, row))
        # self.sprite_entity.set_position()

    def on_select(self):
        pass

    def possible_moves(self):
        pass
