import math
from random import randint

import arcade
import numpy as np

from .tiles import TileDecorator
from config import ASSETS, TREE_ID, OWNED_TILE_HP_CLASS, OWNED_TILE_SALARY


class GameState(object):

    last_mouse_tile_pos = (-1, -1)
    last_mouse_right_tile_pos = (-1, -1)
    last_mouse_tile_texture = ASSETS.hex_textures["GREEN"]
    last_fraction = None

    changed_tiles = dict()
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

    def set_fraction(self, fraction):
        self.last_fraction = fraction

    def set_fractions(self, fractions: list):
        self.fractions = dict()
        for fraction in fractions:
            self.fractions.update({fraction.fraction_id: fraction})

    def append_to_tiles(self, pos, texture):
        self.changed_tiles.update({pos : texture})

    def get_last_fraction(self):
        return self.last_fraction
        # return self.fractions[self.last_fraction]

class HexMap:
    textures_list = {}

    def __init__(self, hex_radius):
        self.hex_radius = hex_radius
        self.hex_size = 0

        self.__margin = 50  # hexagon map start margin

        self.odd_layer_tiles_num = 15
        self.even_layer_tiles_num = self.odd_layer_tiles_num + 1

        self.grid_x_size = self.even_layer_tiles_num
        self.grid_y_size = 20

        self.sprite_tiles = arcade.SpriteList()
        self.tiles = dict()

        # entities on the map
        self.sprite_layer = arcade.SpriteList()
        self.sprites = dict()

        self.MAGICK_X_CONST = 1.84
        self.MAGICK_Y_CONST = 1.63
        # получено опытным путем при исследовании поведения отрисовки картинок Pillow

        self.width, self.height = self.get_window_size()

        # left bottom tile coordinates
        self.map_starts_x = None
        self.map_starts_y = None

        self.state = GameState()

    def initialize_map(self):
        zero_hex = TileDecorator()
        zero_hex.init(self.hex_radius, shiftx=0,
                       shifty=self.__margin, fill_color=arcade.color.GREEN_YELLOW, outline_color="#918585", outline_width=5)

        # посчитать координаты центра первого гексагона
        hex = zero_hex.__copy__()
        hex.shift_right()

        self.map_starts_x = hex.center_x
        self.map_starts_y = hex.center_y

        odd = False
        example = zero_hex.__copy__()
        for y in range(self.grid_y_size - 1, -1, -1):
            if odd:
                example.shift_upper_right()
            elif y != self.grid_y_size - 1:
                example.shift_upper_left()
            sprite = example
            for x in range(self.grid_x_size - 1 - odd, -1, -1):
                sprite = sprite.__copy__()
                sprite.shift_right()
                self.sprite_tiles.append(sprite)
                self.tiles.update(
                    {(self.grid_x_size - x - 1 - odd, self.grid_y_size - y - 1): sprite}
                )
            odd = not odd

        self.hex_size = hex.texture.width
        self.tiles_list = list(self.tiles.keys())

    def create_map(self):
        """
        Создание гексагональной карты и инициализация полей
        :return:
        """
        self.initialize_map()
        # self.place_fractions() <- разместить фракции на карте, задать изначальную территорию
        # self.generate_stuff_on_map()
        # END OF MAP GENERATION

    def draw(self):
        self.sprite_tiles.draw()
        self.sprite_layer.draw()

    def get_window_size(self):
        return (int(self.grid_x_size * self.hex_radius * self.MAGICK_X_CONST),
                int(self.grid_y_size * self.hex_radius * self.MAGICK_Y_CONST))

    def locate(self, x, y):
        """
        Pixel coords to offset coords - do some math
        odd - тот ряд, где меньше гексагонов
        :param x:
        :param y:
        :return:
        """

        def cube_to_offset(x, y, z):
            row = z
            if z + 1 % 2 != 1:  # even row
                col = x + (z - (z & 1)) // 2
            else:  # odd row
                col = x + (z + (z & 1)) // 2
            return col, row

        def cube_round(x, y, z):
            # cube coords
            rx = round(x)
            ry = round(y)
            rz = round(z)

            x_diff = abs(rx - x)
            y_diff = abs(ry - y)
            z_diff = abs(rz - z)

            if x_diff > y_diff and x_diff > z_diff:
                rx = -ry - rz
            elif y_diff > z_diff:
                ry = -rx - rz
            else:
                rz = -rx - ry

            return rx, ry, rz

        x -= self.map_starts_x
        y -= self.map_starts_y

        q = (math.sqrt(3) / 3 * x - 1. / 3 * y) / self.hex_radius
        r = (2. / 3 * y) / self.hex_radius

        point = cube_round(q, -q - r, r)
        return cube_to_offset(*point)

    def unlocate(self, col, row):
        """ Pixel position by offset grid coordinates """
        try:
            tile = self.tiles[(col, row)]
            return tile.center_x, tile.center_y
        except KeyError:
            print(col, row, self.tiles)

    def get_tile(self, row, col):
        return self.tiles[col][row]

    def is_in_map(self, col, row):
        # return (row >= 0 and row < self.grid_y_size and col >= 0 and col < self.grid_x_size)
        return (col, row) in self.tiles

    def count_neighbours(self, col, row):
        """
        6 соседних клеток для гексагона
        :param row:
        :return:
        """
        oddr_directions = [
            [[+1, 0], [0, -1], [-1, -1],
             [-1, 0], [-1, +1], [0, +1]],
            [[+1, 0], [+1, -1], [0, -1],
             [-1, 0], [0, +1], [+1, +1]],
        ]

        dirs = []
        for direction in range(len(oddr_directions[0])):
            parity = row & 1
            dir = oddr_directions[parity][direction]
            col_, row_ = col + dir[0], row + dir[1]
            if self.is_in_map(col_, row_):
                dirs.append((col_, row_))

        dirs.append((col, row))

        return dirs

    def after_init(self, fractions = None):
        """
        Запуск после размещения fractions
        :return:
        """
        # random trees on map
        trees = [self.tiles_list[i] for i in np.unique(np.random.choice(range(0, len(self.tiles_list)), len(self.tiles_list) // 9))]
        self.trees = {}

        fractions_pos = [f.fraction_capital_pos for f in fractions]

        from builders import EntityBuilder, EntityDirector

        director = EntityDirector()
        director.builder = EntityBuilder()
        for i in trees:
            if i not in fractions_pos:
                pos = (self.tiles[i].center_x, self.tiles[i].center_y)
                tree = director.build_entity(entity_type_id=TREE_ID, position=pos).get()
                self.tiles[i].set_entity(tree)
                self.sprite_layer.append(self.tiles[i].sprite_entity)

    def place_fraction(self, fraction):
        """
        Set fraction position and change tiles
        :param fraction:
        :return:
        """
        pos = self.tiles_list[randint(0, len(self.tiles) - 1)]
        self.tiles[pos].set_entity(
            fraction.build_entity(2, pos)
        )

        # Hexmap handle the rednering, so you need to provide access to sprites
        self.sprite_tiles.append(self.tiles[pos].sprite_entity)
        fraction.fraction_capital_pos = pos
        self.tiles[pos].set_tile_fraction(fraction, pos)

        # obj = fraction.build_entity(1, pos)
        # self.spawn_entity(obj, pos, fraction)

        country_tiles = self.count_neighbours(*pos)
        for tile in country_tiles:
            if tile is not None:
                self.tiles[tile].set_tile_texture(fraction.color)
                if self.tiles[tile].entity is None:
                    self.tiles[tile].set_tile_fraction(fraction, tile)

    def spawn_entity(self, entity_id, pos: tuple, fraction):
        """
        Add new sprite to spritelist
        :param pos:
        :param id:
        :return:
        """
        # try:
        if pos in fraction.tiles.keys(): # спавн только на собственных территориях
            entity = self.tiles[pos].entity
            if self.tiles[pos].is_owned_tile():
                if self.tiles[pos].owned.fraction_id != fraction.fraction_id:
                    return False

            if entity is None or entity.entity_id < 0: # TODO UNCOMMENT
                if entity is not None and entity.entity_id == TREE_ID:
                    fraction.money_amount -= entity.salary  # todo add price instead of salary
                    self.tiles[pos].sprite_entity.remove_from_sprite_lists()
            else:
                return False
            obj = fraction.build_entity(entity_id, pos)
            self.tiles[pos].set_entity(obj)
            self.sprite_tiles.append(self.tiles[pos].sprite_entity)
            return True
        return False

    def get_move_range(self, old_pos):
        out = set()
        for tile in self.count_neighbours(old_pos[0], old_pos[1]):
            out.update(set(self.count_neighbours(tile[0], tile[1])))

        tiles = set()
        for tile in self.state.get_last_fraction().tiles.keys():
            if tile in out:
                tiles.update(set(self.count_neighbours(tile[0], tile[1])))

        return list(tiles)
        # return list(out)

    def show_move_range(self, old_pos, color, color2):
        from config import COLORS
        for new_pos in self.get_move_range(old_pos):
            if self.is_in_move_range(old_pos, new_pos) and new_pos != old_pos:
                if self.tiles[old_pos].can_move(self.tiles[new_pos]):
                    self.state.changed_tiles.update({new_pos : self.tiles[new_pos].get_tile_texture()})
                    if self.tiles[new_pos].is_own(self.state.get_last_fraction()):
                        self.tiles[new_pos].set_tile_texture(color) # color2
                    else:
                        self.tiles[new_pos].set_tile_texture(color)
            elif new_pos == old_pos:
                self.tiles[new_pos].set_tile_texture(color) # color2

    def add_tile_to_state(self, pos):
        self.state.changed_tiles.update({pos: self.tiles[pos].get_tile_texture()})

    def select_tile(self, pos, color):
        self.tiles[pos].set_tile_texture(color)

    def unselect_tiles(self):
        for (pos, texture) in self.state.changed_tiles.items():
            self.tiles[pos].update_tile_texture(texture)
        self.state.changed_tiles.clear()

    def is_in_move_range(self, old, new):
        return new in self.get_move_range(old)

    def move_unit(self, old_pos, new_pos):
        # tile = self.tiles[old_pos]
        # if not tile.is_empty() and tile.is_used():
        #     return False, False
        # print(tile)

        if old_pos == new_pos:
            return False, False

        if self.is_in_move_range(old_pos, new_pos):
            tile = self.tiles[new_pos]
            fraction_id = tile.get_tile_fraction_id()

            if not tile.is_empty():
                is_tree = tile.entity.entity_id == TREE_ID
                if is_tree:
                    self.state.get_last_fraction().money_amount -= tile.entity.cost  # todo add price instead of salary
                if not is_tree and tile.entity.fraction_id == self.state.get_last_fraction().fraction_id:
                    # попытка перейти на свою занятую клетку
                    return False, False
                delta = self.tiles[new_pos].kill_entity()
                if fraction_id > 0:
                    self.state.fractions[fraction_id].update_step_delta(delta)

            moved = self.tiles[old_pos].move_to(new_pos, tile) # grid pos, tile
            if moved:
                move_in_own_tiles = fraction_id == self.state.get_last_fraction().fraction_id
                if fraction_id > 0:
                    tile.set_tile_fraction(self.state.get_last_fraction(), new_pos, self.state.fractions[fraction_id])
                else:
                    tile.set_tile_fraction(self.state.get_last_fraction(), new_pos)

                # if not move_in_own_tiles:
                #     if fraction_id > 0:
                #         self.state.fractions[fraction_id].update_step_delta(-OWNED_TILE_SALARY)
                #     self.state.get_last_fraction().update_step_delta(OWNED_TILE_SALARY)
                return True, move_in_own_tiles
        return False, False

    def set_defence(self, new_pos, old_pos = None):
        unit = self.tiles[new_pos]
        fraction = self.state.get_last_fraction()

        if unit.entity.damage_range == 1:
            # Защита клеток: класс здоровья соседних в радиусе 1 становится таким же, как и у юнита
            if old_pos:
                prev_neighbours = self.count_neighbours(old_pos[0], old_pos[1])
                for tile in prev_neighbours:
                    if self.tiles[tile].is_own(fraction):
                        self.tiles[tile].set_tile_health(OWNED_TILE_HP_CLASS)

            neighbours = self.count_neighbours(new_pos[0], new_pos[1])
            for tile in neighbours:
                if self.tiles[tile].is_own(fraction):
                    self.tiles[tile].set_tile_health(self.tiles[new_pos].entity.health)

    def unuse_entity(self, tile):
        self.tiles[tile].unuse_entity()

    def use_entity(self, tile):
        self.tiles[tile].use_entity()

    def get_gold_delta(self, tile):
        return self.tiles[tile].get_gold_delta()


