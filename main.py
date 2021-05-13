import arcade
import time

from config import FRACTIONS_CONFIG, MAP_HEX_RADIUS, ENTITY_ID2COST
from control import SpawnEntity, NextStep, UpdateGameState, MoveUnit
from fractions import Fraction
from game_state import GameState
from map.hexagonal_map import HexMap

from arcade.gui import UIManager
from ui import set_ui, update_ui

has_exit = False

class Bot:
    def make_move(self, position):
        pass

    def get_state(self):
        return [{'command' : "move"}]

class Game(arcade.Window):
    # Играют по очереди, сначала делает ход первый игрок, потом второй и т.д.
    hosts: list = []  # список хостов (фракций) игроков (хост - играбельный объект, т.е. страна)
    hosts_num = 2
    active_host: int  # номер текущего активного хоста (тот, который играет)
    game_iteration: int  # номер хода

    host_init_pos = {1: (1, 10), 0: (8, 1)}

    gamer_host: int

    state = None
    select_color = "BLUE"
    select2_color = "COLUMBIA_BLUE"

    ui_margin_left = None
    ui_margin_top = None

    game_over = False

    bot = None

    def __init__(self):
        self.state = GameState()
        self.map = HexMap(hex_radius=MAP_HEX_RADIUS)
        self.w, self.h = self.map.get_window_size()
        super().__init__(self.w + self.w // 4, self.h, "Poliyoy")

        arcade.set_background_color(arcade.color.BLACK)

        self.ui_manager = UIManager()
        self.ui_margin_left = self.w / 15
        self.ui_margin_top = self.h / 10

        self.bot = Bot()

        self.game_iteration = 0

        self.setup()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def init_hosts(self):
        for (e, frac) in enumerate(FRACTIONS_CONFIG.keys()):
            self.hosts.append(Fraction(**FRACTIONS_CONFIG[frac]))

            fraction = self.hosts[-1]
            self.state.append_fraction(fraction)

            if not fraction.isBot:
                self.active_host = e
                self.gamer_host = e

            self.map.place_fraction(fraction, self.host_init_pos[fraction.fraction_id])

        self.state.set_fraction(self.gamer_host)

    def setup(self):
        """
        Здесь рендеринг UI и инициализация пользовательской fraction
        Например, разместить сущности стран на карте
        :return:
        """

        self.map.create_map()
        self.init_hosts()
        self.after_init()  # размещение на карте деревьев и т.п.
        # self.map.after_init(self.hosts)  # размещение на карте деревьев и т.п.

        self.ui_manager.purge_ui_elements()
        set_ui(self)

    def after_init(self):
        """
        Запуск после размещения fractions
        :return:
        """
        trees = self.map.get_random_positions()
        from config import TREE_ID
        fr = self.state.get_last_fraction()
        for i in trees:
            self.map.spawn_tree(i, fr)

    def on_draw(self):
        """
        Рендеринг различных объектов
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        self.map.draw()
        self.ui_manager.on_draw()

    def on_next_step_key_press(self):
        from transmitters import PlayerStateTransmitterHandler

        for host in self.hosts:
            for tile in host.tiles:
                self.map.unuse_entity(tile)

        self.game_over = self.state.get_last_fraction().make_step() # user

        # Turn to bot
        self.active_host = not self.active_host
        self.state.set_fraction(self.active_host)  # upd last host

        # test = PlayerStateTransmitterHandler().forward(self.state.get_last_fraction(), self.state.fractions[not self.active_host])[1]
        # print(test.money, test.cells, test.money, test.archers, test.strong_units, test.spawned_villages, test.defence_towers)
        self.bot.make_move(PlayerStateTransmitterHandler().forward(self.state.get_last_fraction(), self.state.fractions[not self.active_host]))
        self.bot_command_parser(self.bot.get_state())
        self.game_over = self.state.get_last_fraction().make_step() # bot

        # Turn to player
        self.active_host = not self.active_host
        self.state.set_fraction(self.active_host)
        self.update_screen_info()
        self.update_village_btn()
        self.game_iteration += 1

    def update_screen_info(self):
        self.ui_manager.find_by_id("money_amount").text = "Gold: " + str(self.state.get_last_fraction().money_amount)
        self.ui_manager.find_by_id("money_step").text = "Delta: " + str(self.state.get_last_fraction().step_delta)

    def update_village_btn(self):
        # Тяжелая операция, поэтому случай обрабатывается отдельно
        # # Дальше костыль для обновления текста кнопки (в либе такое, почему-то, не предусмотрено)
        update_ui(self)

    def move_unit(self, host):
        pos = self.state.last_mouse_right_tile_pos
        unit_pos = self.state.last_mouse_tile_pos
        if unit_pos in host.units_pos.keys():
            self.state.last_mouse_right_tile_pos = pos
            command = MoveUnit(self.map, self.state, UpdateGameState(self))
            command.execute()

        if pos in host.tiles.keys():
            pass

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Обработка пользовательского действия
        """
        col, row = self.map.locate(x, y)
        host = self.state.get_last_fraction()
        pos = (col, row)

        self.map.unselect_tiles()

        if button == 1:
            if self.map.is_in_map(col, row):
                self.map.add_tile_to_state(pos)
                self.map.select_tile(pos, self.select_color)

                self.state.set_pos(col, row)

                if pos in host.units_pos.keys():
                    self.map.show_move_range(pos, self.select_color, self.select2_color)

        elif button == 4:
            self.state.last_mouse_right_tile_pos = pos
            self.move_unit(host)

    def possible_moves(self, pos):
        return self.map.show_move_range_quiet(pos)

    def bot_command_parser(self, move_list):
        for move in move_list:
            command = move['command']
            if command == 'create_village':
                col, row = move[1][0], move[1][1]
                self.state.set_pos(col, row)
                self.ui_manager.find_by_id("village").on_click()
            elif command == 'create_archer':
                col, row = move[1][0], move[1][1]
                self.state.set_pos(col, row)
                self.ui_manager.find_by_id("scout").on_click()
            elif command == 'create_strong_unit':
                col, row = move[1][0], move[1][1]
                self.state.set_pos(col, row)
                self.ui_manager.find_by_id("warrior").on_click()
            elif command == 'create_defence_tower':
                col, row = move[1][0], move[1][1]
                self.state.set_pos(col, row)
                self.ui_manager.find_by_id("tower").on_click()
            elif command == 'move_archer' or command == 'move_strong_unit':
                old_col, old_row = move[1][0], move[1][1]
                col, row = move[1][0], move[1][1]
                self.state.set_pos(old_col, old_row)
                self.state.last_mouse_right_tile_pos = (col, row)
                self.move_unit(self.state.get_bot_fraction())


class GameEnvironment():
    def __init__(self):
        self.game_window = None
        self.set_game_window()

    def set_game_window(self):
        self.game_window = Game()

    def is_over(self):
        return self.game_window.game_over


def game_loop(game_obj):
    global has_exit

    game_iters = 0
    start_time = time.time()
    while not game.is_over():
        if has_exit:
            break

        game.game_window.switch_to()
        game.game_window.dispatch_events()
        game.game_window.dispatch_event('on_draw')
        game.game_window.flip()

        game_iters = game.game_window.game_iteration

        current_time = time.time()
        elapsed_time = current_time - start_time
        start_time = current_time
        if elapsed_time < 1. / 60.:
            sleep_time = (1. / 60.) - elapsed_time
            time.sleep(sleep_time)
        game.game_window._dispatch_updates(1 / 60)

        game.nplayer = game.game_window.active_host + 1


if __name__ == "__main__":
    game = GameEnvironment()
    has_exit = False

    @game.game_window.event
    def on_close():
        global has_exit
        print("Game over")
        has_exit = True

    game_loop(game)



