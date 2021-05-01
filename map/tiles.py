from arcade import Sprite, SpriteList
from .hexagonal import Hex
from abstract import AbstractEntity
from entity import OwnedTile
from fractions import Fraction
from config import ASSETS, COLORS, TREE_ID, OWNED_TILE_ID


class TileDecorator(Hex):
    """
    Декоратор объекта Hex
    """

    entity: AbstractEntity = None
    owned: OwnedTile = None
    sprite_entity: Sprite = None

    def __init__(self, *args, **kwargs) -> None:
        super(TileDecorator, self).__init__(*args, **kwargs)

    def is_empty(self):
        return self.entity is None

    def get_sprite(self):
        return self.sprite_entity

    def set_entity(self, entity: AbstractEntity = None) -> None:
        self.entity = entity
        # if self.is_owned_tile():
        self.sprite_entity = Sprite(ASSETS.entities_textures[entity.entity_id], entity.texture_scale)
        self.sprite_entity.set_position(self.center_x, self.center_y)
        self.sprite_entity._points = None
        self.entity.used_in_step = False

    def set_tile_texture(self, texture_id):
        try:
            self.texture = ASSETS.hex_textures[texture_id]
        except KeyError:
            raise NotImplementedError

    def set_tile_fraction(self, new_fraction : Fraction, pos, old_fraction : Fraction = None):
        if new_fraction == old_fraction:
            return
        if old_fraction is not None:
            old_fraction.detach_tile(pos)
        self.owned = new_fraction.build_entity(OWNED_TILE_ID, pos)
        self.set_tile_texture(new_fraction.color)

    def get_tile_texture(self):
        return self.texture

    def get_tile_fraction_id(self):
        if self.is_owned_tile():
            return self.owned.fraction_id
        return -1

    def get_tile_health(self):
        if self.is_owned_tile():
            return self.owned.health

    def set_tile_health(self, hp):
        if self.is_owned_tile():
            self.owned.health = hp

    def update_tile_texture(self, texture):
        self.texture = texture

    def is_one_fraction(self, oth):
        return self.owned.fraction_id == oth.owned.fraction_id

    def can_move(self, oth_tile):
        # можно ли переместиться на oth_tile

        if self.is_empty() or self.entity.entity_id < 0:  # пустая клетка или дерево (лол)
            return False

        if oth_tile.owned is not None:
            if not self.is_one_fraction(oth_tile):
                return oth_tile.get_tile_health() < self.entity.damage

        if oth_tile.is_empty() or oth_tile.entity.entity_id < 0:
            return True

        if not oth_tile.is_empty() and oth_tile.is_owned_tile() and self.is_one_fraction(oth_tile):
            return True

        if not oth_tile.is_empty():
            if not self.is_one_fraction(oth_tile):
                return oth_tile.entity.health < self.entity.damage

        return False

    def is_owned_tile(self):
        return self.owned is not None
        # return self.entity.entity_id == OWNED_TILE_ID

    def is_own(self, fraction_obj: Fraction):
        if self.is_owned_tile():
            return fraction_obj.fraction_id == self.owned.fraction_id
        return False

    def is_used(self):
        return self.entity.used_in_step

    def move_to(self, pos, oth_tile):
        if not self.can_move(oth_tile):
            return False

        if oth_tile.is_owned_tile() or oth_tile.is_empty():
            if self.is_used():
                print("ENTITY USED IN STEP")
                return False
            oth_tile.sprite_entity = self.sprite_entity
            oth_tile.entity = self.entity
            oth_tile.entity.move_to(pos)
            oth_tile.sprite_entity.set_position(oth_tile.center_x, oth_tile.center_y)
            self.use_entity()

        self.entity = None
        self.sprite_entity = None
        return True

    def kill_entity(self):
        delta = self.entity.salary
        self.entity = None
        self.sprite_entity.remove_from_sprite_lists()
        return delta


    def use_entity(self):
        if not self.is_empty():
            self.entity.used_in_step = True

    def unuse_entity(self):
        if not self.is_empty():
            self.entity.used_in_step = False

    # def get_gold_delta(self):
    #     delta = 0
    #     # if not self.is_empty():
    #     #     delta += self.entity.salary
    #     if self.is_owned_tile():
    #         delta += self.owned.salary
    #     return delta

    def on_select(self):
        pass

    def possible_moves(self):
        pass
