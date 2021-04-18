import arcade
from arcade.gui import UIFlatButton, UIGhostFlatButton, UIManager
from map.hexagonal_map import HexMap, MapState
from arcade.gui.ui_style import UIStyle
from fractions import Fraction
from config import FRACTIONS_CONFIG, MAP_HEX_RADIUS, ASSETS
from ui import PlaceEnityButton


class Game(arcade.Window):
    # Играют по очереди, сначала делает ход первый игрок, потом второй и т.д.
    hosts: list = []  # список хостов (фракций) игроков (хост - играбельный объект, т.е. страна)
    hosts_num = 2
    active_host: int  # номер текущего активного хоста (тот, который играет)
    game_iteration: int  # номер хода

    map_state = None
    select_color = "BLUE"

    ui_margin_left = None
    ui_margin_top = None

    def __init__(self):
        self.map_state = MapState()
        self.map = HexMap(hex_radius=MAP_HEX_RADIUS)
        self.w, self.h = self.map.get_window_size()
        super().__init__(self.w + self.w // 6, self.h, "Poliyoy")

        arcade.set_background_color(arcade.color.BLACK)

        self.ui_manager = UIManager()

        self.ui_margin_left = self.w / 30
        self.ui_margin_top = self.h / 10

        self.setup()

    def init_hosts(self):
        for (e, frac) in enumerate(FRACTIONS_CONFIG.keys()):
            self.hosts.append(Fraction(**FRACTIONS_CONFIG[frac]))
            fraction = self.hosts[-1]

            if not fraction.isBot:
                self.hosts_num = e

            self.map.place_fraction(fraction)

    def setup(self):
        """
        Здесь рендеринг UI и инициализация пользовательской fraction
        Например, разместить сущности стран на карте
        :return:
        """

        from control import SpawnEntity

        self.map.create_map()
        self.init_hosts()
        self.map.after_init(self.hosts) # размещение на карте деревьев и т.п.

        self.ui_manager.purge_ui_elements()
        btn = PlaceEnityButton(text="V", center_x=self.w + self.ui_margin_left, # village
                            center_y=self.h - self.ui_margin_top, width=50, height=50)
        btn.set_command(SpawnEntity(self.map, self.map_state, 2))
        self.ui_manager.add_ui_element(btn)

    def on_draw(self):
        """
        Рендеринг различных объектов
        Например, self.hosts[0].render() - рендерит клетки страны
        и сущности страны на карте
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        self.map.draw()
        self.ui_manager.on_draw()

    def select_tile(self, col, row):
        tile = self.map.tiles[(col, row)]
        # if not tile.is_empty():
        tile.set_tile_texture(self.select_color)

    def unselect_tile(self, col, row):
        lcol, lrow = self.map_state.last_mouse_tile_pos
        if col == lcol and lrow == row:
            return False
        elif self.map.is_in_map(lcol, lrow):
            tile = self.map.tiles[self.map_state.last_mouse_tile_pos]
            # if not tile.is_empty():
            tile.texture = self.map_state.last_mouse_tile_texture
            # tile.set_tile_texture("GREEN")
            return True
        return True

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Обработка пользовательского действия
        """
        col, row = self.map.locate(x, y)
        host = self.hosts[self.hosts_num]

        print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({col}, {row})")

        flag = self.unselect_tile(col, row)

        old_texture = None
        if self.map.is_in_map(col, row):
            old_texture = self.map.tiles[(col, row)].texture
            self.select_tile(col, row)

            if flag:
                self.map_state.set_pos(col, row)
                self.map_state.set_texture(old_texture)

        self.map_state.set_fraction(self.hosts[self.hosts_num]) # upd last host

    # def on_mouse_motion(self, x, y, dx, dy):
    #     print(x, y, dx, dy)
    #     col, row = self.map.locate(x, y)
    #     lcol, lrow = col + dx, row + dy
    #
    #     if lcol != col and lrow != row:
    #         if self.map.is_in_map(lcol, lrow):
    #             tile = self.map.tiles[(lcol, lrow)]
    #             tile.set_tile_texture("GREEN")
    #
    #     # last_col, last_row = self.map.locate()
    #     if self.map.is_in_map(col, row):
    #         tile = self.map.tiles[(col, row)]
    #
    #         # if not tile.is_empty():
    #         tile.set_tile_texture("BLUE")


    def bot_move(self):
        pass


if __name__ == "__main__":
    Game()
    arcade.run()

    # a = arcade.Sprite()
    # a.textures
