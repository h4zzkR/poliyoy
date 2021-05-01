import arcade
from arcade.gui import UIFlatButton, UIGhostFlatButton, UIManager
from map.hexagonal_map import HexMap, GameState
from arcade.gui.ui_style import UIStyle
from fractions import Fraction
from config import FRACTIONS_CONFIG, MAP_HEX_RADIUS, ASSETS
from ui import PlaceEntityButton, NextStepButton
from control import MoveUnit


class Game(arcade.Window):
    # Играют по очереди, сначала делает ход первый игрок, потом второй и т.д.
    hosts: list = []  # список хостов (фракций) игроков (хост - играбельный объект, т.е. страна)
    hosts_num = 2
    active_host: int  # номер текущего активного хоста (тот, который играет)
    game_iteration: int  # номер хода

    gamer_host: int

    map_state = None
    select_color = "BLUE"
    select2_color = "COLUMBIA_BLUE"

    ui_margin_left = None
    ui_margin_top = None

    def __init__(self):
        self.map_state = GameState()
        self.map = HexMap(hex_radius=MAP_HEX_RADIUS)
        self.w, self.h = self.map.get_window_size()
        super().__init__(self.w + self.w // 6, self.h, "Poliyoy")

        arcade.set_background_color(arcade.color.BLACK)

        self.ui_manager = UIManager()

        self.ui_margin_left = self.w / 30
        self.ui_margin_top = self.h / 10

        self.setup()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def init_hosts(self):
        for (e, frac) in enumerate(FRACTIONS_CONFIG.keys()):
            self.hosts.append(Fraction(**FRACTIONS_CONFIG[frac]))
            fraction = self.hosts[-1]
            self.map_state.set_fraction(fraction)

            if not fraction.isBot:
                self.active_host = e
                self.gamer_host = e

            self.map.place_fraction(fraction)

        self.map_state.set_fractions(self.hosts)
        self.map_state.set_fraction(self.hosts[self.active_host])

    def setup(self):
        """
        Здесь рендеринг UI и инициализация пользовательской fraction
        Например, разместить сущности стран на карте
        :return:
        """

        from control import SpawnEntity, NextStep

        btn_w, btn_h = 50,50

        self.map.create_map()
        self.init_hosts()
        self.map.after_init(self.hosts) # размещение на карте деревьев и т.п.

        self.ui_manager.purge_ui_elements()

        next_btn = NextStepButton(text="Step", center_x=self.w + 2 * self.ui_margin_left,
                                  center_y=self.h - self.ui_margin_top, width=btn_w * 2.1, height=btn_h)
        next_btn.set_command(NextStep(self))
        self.ui_manager.add_ui_element(next_btn)

        btn1 = PlaceEntityButton(text="V", center_x=self.w + self.ui_margin_left,  # village
                                center_y=next_btn.center_y - 1.2 * btn_h, width=btn_w, height=btn_h)
        btn1.set_command(SpawnEntity(self.map, self.map_state, 2))
        self.ui_manager.add_ui_element(btn1)

        btn2 = PlaceEntityButton(text="S", center_x=btn1.center_x + btn_w * 1.2,  # village
                                center_y=btn1.center_y, width=btn_w, height=btn_h)
        btn2.set_command(SpawnEntity(self.map, self.map_state, 1))
        self.ui_manager.add_ui_element(btn2)

        money_label = arcade.gui.UILabel(
            f'Gold: {self.hosts[self.gamer_host].money_amount}',
            center_x=btn1.center_x + btn_w * 0.55,
            center_y=btn1.center_y - btn_h,
            id="money_amount"
        )
        self.ui_manager.add_ui_element(money_label)

        money_step = arcade.gui.UILabel(
            f'Delta: {self.hosts[self.gamer_host].step_delta}',
            center_x=money_label.center_x,
            center_y=money_label.center_y - btn_h * 0.65,
            id="money_step"
        )
        self.ui_manager.add_ui_element(money_step)



        # from control import SpawnEntity
        # back = self.map_state.last_mouse_tile_pos
        # back2 = self.map_state.last_fraction
        # self.map_state.last_mouse_tile_pos = self.hosts[not self.active_host].fraction_capital_pos
        # self.map_state.last_fraction = self.hosts[not self.active_host]
        # obj = SpawnEntity(self.map, self.map_state, 1)
        # obj.execute()
        # self.map_state.last_mouse_tile_pos = back
        # self.map_state.last_fraction = back2

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

    def on_next_step_key_press(self):
        # print("before", self.hosts[1].money_amount)
        for host in self.hosts:
            for tile in host.tiles:
                self.map.unuse_entity(tile)
        self.hosts[1].make_step()
        self.update_screen_info()

    def update_screen_info(self):
        self.ui_manager.find_by_id("money_amount").text = "Gold: " + str(self.hosts[self.gamer_host].money_amount)
        self.ui_manager.find_by_id("money_step").text = "Delta: " + str(self.hosts[self.gamer_host].step_delta)

    def update_game_state(self):
        for host in self.hosts:
            host.update_state()

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Обработка пользовательского действия
        """
        col, row = self.map.locate(x, y)
        host = self.hosts[self.active_host]
        pos = (col, row)

        self.map.unselect_tiles()

        if button == 1:
            if self.map.is_in_map(col, row):
                self.map.add_tile_to_state(pos)
                self.map.select_tile(pos, self.select_color)

                self.map_state.set_pos(col, row)

                if pos in host.units_pos.keys():
                    self.map.show_move_range(pos, self.select_color, self.select2_color)

        elif button == 4:
            unit_pos = self.map_state.last_mouse_tile_pos
            if unit_pos in host.units_pos.keys():
                self.map_state.last_mouse_right_tile_pos = pos
                command = MoveUnit(self.map, self.map_state)
                command.execute()

            if pos in host.tiles.keys():
                pass

        # self.map_state.set_fraction(self.hosts[(self.active_host + 1) % 2]) # upd last host
        self.map_state.set_fraction(self.hosts[self.active_host]) # upd last host
        self.update_game_state()

    def bot_move(self):
        pass


if __name__ == "__main__":
    Game()
    arcade.run()

    # a = arcade.Sprite()
    # a.textures
