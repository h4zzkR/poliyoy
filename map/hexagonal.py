import math

import arcade
from arcade import Sprite
from draw import make_hexagon_texture


class Hex(Sprite):

    def __init__(self):
        super(Hex, self).__init__()

    def init(self, size=None, center_point=(0, 0), shiftx=0, shifty=0,
             fill_color=arcade.color.GREEN, outline_width=5, outline_color="#918585"):
        self.size = size
        self.outline_width = outline_width
        self.fill_color = fill_color
        self.outline_color = outline_color
        self.outline_width = outline_width

        self.init_position(center_point, shiftx, shifty)

    def init_position(self, center_point, shiftx, shifty):
        center_pos = center_point  # абсолютный центр (на плоскости)

        self.hmargin = self.get_width()  # horizontal
        self.vmargin = self.get_height() * 3 / 4  # vertical

        self.cpoints = []  # границы hex
        for i in range(6):
            coords = self.hex_corner(i, center_pos)
            self.cpoints.append((coords[0], coords[1]))

        self.texture = make_hexagon_texture(self.size, self.fill_color,
                                            self.cpoints, self.outline_color, self.outline_width)
        self._points = self.cpoints

        self.center_x = center_pos[0] + shiftx
        self.center_y = center_pos[1] + shifty

    def hex_corner(self, i, center_pos):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        return (center_pos[0] + self.size * math.cos(angle_rad),
                center_pos[1] + self.size * math.sin(angle_rad))

    def set_corners(self, center_pos):
        for i in range(6):
            coords = self.hex_corner(i, center_pos)
            self.cpoints.append((coords[0], coords[1]))

    def get_width(self):
        return self.size * math.sqrt(3)

    def get_height(self):
        return self.size * 2

    def shift_position(self, shiftx, shifty):
        self.set_position(self.position[0] + shiftx, self.position[1] + shifty)

    def shift_right(self, margin=0):
        self.set_position(self.position[0] + self.hmargin + margin, self.position[1] + margin)

    def shift_left(self, margin=0):
        self.set_position(self.position[0] - (self.hmargin + margin), self.position[1] + margin)

    def shift_upper_right(self, margin=0):
        self.set_position(self.position[0] + self.hmargin / 2 + margin, self.position[1] + self.vmargin + margin)

    def shift_upper_left(self, margin=0):
        self.set_position(self.position[0] - (self.hmargin / 2 + margin), self.position[1] + self.vmargin + margin)

    def shift_up(self, margin=0):
        self.set_position(self.position[0], self.position[1] + self.vmargin * 2 + margin)

    def shift_down(self, margin=0):
        self.set_position(self.position[0], self.position[1] - (self.vmargin * 2 + margin))

    def __copy__(self):
        obj = self.__class__()
        obj.color = self.color
        obj.size = self.size
        obj.cpoints = self.cpoints
        obj.center_y = self.center_y
        obj.center_x = self.center_x
        obj.outline_width = self.outline_width
        obj._points = self._points
        obj.outline_color = self.outline_color
        obj.texture = self.texture
        obj.vmargin = self.vmargin
        obj.hmargin = self.hmargin
        obj.position = self.position
        obj.__dict__.update(self.__dict__)
        return obj