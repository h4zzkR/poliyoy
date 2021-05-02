from arcade.gui import UIFlatButton, UIManager
import arcade
import time

from easyAI import TwoPlayersGame, Human_Player, AI_Player, Negamax

from config import FRACTIONS_CONFIG, MAP_HEX_RADIUS, ENTITY_ID2COST
from control import SpawnEntity, NextStep, UpdateGameState, MoveUnit
from fractions import Fraction
from game_state import GameState
from map.hexagonal_map import HexMap

from arcade.gui import UIManager
from ui import set_ui, update_ui


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

    game_over = False

    def __init__(self):
        self.map_state = GameState()
        self.map = HexMap(hex_radius=MAP_HEX_RADIUS)
        self.w, self.h = self.map.get_window_size()
        super().__init__(self.w + self.w // 4, self.h, "Poliyoy")

        arcade.set_background_color(arcade.color.BLACK)

        self.ui_manager = UIManager()
        self.ui_margin_left = self.w / 15
        self.ui_margin_top = self.h / 10

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
            self.map_state.append_fraction(fraction)

            if not fraction.isBot:
                self.active_host = e
                self.gamer_host = e

            self.map.place_fraction(fraction)

        self.map_state.set_fraction(self.gamer_host)

    def setup(self):
        """
        Здесь рендеринг UI и инициализация пользовательской fraction
        Например, разместить сущности стран на карте
        :return:
        """

        self.map.create_map()
        self.init_hosts()
        self.map.after_init(self.hosts)  # размещение на карте деревьев и т.п.

        self.ui_manager.purge_ui_elements()
        set_ui(self)

        # back = self.map_state.last_mouse_tile_pos
        # back2 = self.map_state.last_fraction
        # self.hosts[not self.active_host].money_amount = 9999
        #
        # pos = self.hosts[not self.active_host].fraction_capital_pos
        # self.map_state.last_mouse_tile_pos = pos
        # self.map_state.last_fraction = self.hosts[not self.active_host]
        # obj = SpawnEntity(self.map, self.map_state, 1, UpdateGameState(self))
        # obj.execute()
        # self.map_state.last_mouse_tile_pos = back
        # self.map_state.last_fraction = back2
        # sys.exit()

    def on_draw(self):
        """
        Рендеринг различных объектов
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
        game_over = self.hosts[0].make_step()
        game_over = self.hosts[1].make_step()
        self.update_screen_info()
        if game_over:
            self.game_over = True

        self.game_iteration += 1

        self.active_host = not self.active_host
        self.map_state.set_fraction(self.active_host)  # upd last host

    def update_screen_info(self):
        self.ui_manager.find_by_id("money_amount").text = "Gold: " + str(self.hosts[self.gamer_host].money_amount)
        self.ui_manager.find_by_id("money_step").text = "Delta: " + str(self.hosts[self.gamer_host].step_delta)

    def update_village_btn(self):
        # Тяжелая операция, поэтому случай обрабатывается отдельно
        # # Дальше костыль для обновления текста кнопки (в либе такое, почему-то, не предусмотрено)
        update_ui(self)

    def on_mouse_press(self, x, y, button, modifiers):
        """
        Обработка пользовательского действия
        """
        col, row = self.map.locate(x, y)
        host = self.map_state.get_last_fraction()
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
                command = MoveUnit(self.map, self.map_state, UpdateGameState(self))
                command.execute()

            if pos in host.tiles.keys():
                pass

        # print(self.active_host, self.map_state.get_last_fraction().fraction_id)

    def bot_move(self):
        pass


class GameEnvironment(TwoPlayersGame):
    def __init__(self, players):
        self.players = players
        self.pile = 20  # start with 20 bones in the pile
        self.nplayer = 1  # player 1 starts
        self.game_window = None
        self.set_game_window()

    def set_game_window(self):
        self.game_window = Game()
        self.nplayer = self.game_window.gamer_host + 1

    def possible_moves(self): return ['1', '2', '3']

    def make_move(self, move): self.pile -= int(move)  # remove bones.

    def win(self): return self.pile <= 0  # opponent took the last bone ?

    # def is_over(self): return self.win() # Game stops when someone wins.
    def is_over(self):
        return self.game_window.game_over

    def show(self): print("%d bones left in the pile" % self.pile)

    def scoring(self): return 100 if game.win() else 0  # For the AI


if __name__ == "__main__":
    game = GameEnvironment([Human_Player(), AI_Player(Negamax(9))])
    has_exit = False


    @game.game_window.event
    def on_close():
        global has_exit
        print("Game over")
        has_exit = True


    game_iters = 0

    start_time = time.time()
    while not game.is_over():
        if has_exit:
            break
        # game.show()
        # if game.nplayer == 1:  # we are assuming player 1 is a Human_Player
        #     poss = game.possible_moves()
        #     for index, move in enumerate(poss):
        #         print("{} : {}".format(index, move))
        #     index = int(input("enter move: "))
        #     move = poss[index]
        # else:  # we are assuming player 2 is an AI_Player
        #     move = game.get_move()
        #     print("AI plays {}".format(move))
        #
        # game.play_move(move)

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
