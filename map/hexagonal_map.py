import math
from random import randint

import arcade
import numpy as np
from arcade import Sprite

from .tiles import TileDecorator
from config import ASSETS


class MapState(object):

    last_mouse_tile_pos = (-1, -1)
    last_mouse_tile_texture = ASSETS.hex_textures["GREEN"]
    last_fraction = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MapState, cls).__new__(cls)
        return cls.instance

    def set_pos(self, col, row):
        self.last_mouse_tile_pos = (col, row)

    def set_texture(self, texture):
        self.last_mouse_tile_texture = texture

    def set_fraction(self, fraction):
        self.last_fraction = fraction

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

    def after_init(self, fractions = None):
        """
        Запуск после размещения fractions
        :return:
        """
        # random trees on map
        trees = [self.tiles_list[i] for i in np.random.choice(range(0, len(self.tiles_list)), len(self.tiles_list) // 9)]
        self.trees = {}

        fractions_pos = [f.fraction_capital_pos for f in fractions]
        for i in trees:
            if i not in fractions_pos:
                pos = (self.tiles[i].center_x, self.tiles[i].center_y)
                # tree_tile = self.tiles[pos]
                tree = Sprite("./assets/tree.png", 0.08)
                tree.set_position(*pos)
                self.sprite_layer.append(tree)
                self.trees.update({i: tree})

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
            else:
                dirs.append(None)

        dirs.append((col, row))

        return dirs

    def place_fraction(self, fraction):
        """
        Set fraction position and change tiles
        :param fraction:
        :return:
        """
        pos = self.tiles_list[randint(0, len(self.tiles) - 1)]
        self.tiles[pos].set_entity(
            fraction.entity_director.set_fraction(fraction.fraction_id).build_village((self.unlocate(*pos))).get()
        )

        # Hexmap handle the rednering, so you need to provide access to sprites
        self.sprite_tiles.append(self.tiles[pos].sprite_entity)

        fraction.entities.update({ pos: self.tiles[pos].entity })
        fraction.fraction_capital_pos = pos
        #
        country_tiles = self.count_neighbours(*pos)
        for tile in country_tiles:
            if tile is not None:
                self.tiles[tile].set_tile_texture(fraction.color)

    def spawn_entity(self, obj, pos: tuple):
        """
        Add new sprite to spritelist
        :param pos:
        :param id:
        :return:
        """
        try:
            self.tiles[pos].set_entity(obj)
        except Exception:
            return
        self.sprite_tiles.append(self.tiles[pos].sprite_entity)