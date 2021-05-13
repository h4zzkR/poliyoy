from new_bot import Bot
from field import Position, PlayerPosition, HexagonalField


def bfs(field, this_cell, count):
    used_cells = set(this_cell)
    answer = [this_cell]
    active_cells = [this_cell]
    while True:
        next_active_cells = []
        for i in active_cells:
            cells = field.get_neighbour(i[0], i[1])
            for j in cells:
                if not (j in used_cells):
                    used_cells.add(j)
                    next_active_cells.append(j)
                    answer.append(j)
                    if len(answer) == count:
                        return answer
        active_cells = next_active_cells.copy()


class Game:
    first_bot = Bot(None)
    second_bot = Bot(None)
    position = Position(PlayerPosition(None), PlayerPosition(None), HexagonalField())

    def __init__(self, bot1, bot2):
        self.first_bot = bot1
        self.second_bot = bot2

        field = HexagonalField()
        first_bot_cell = [0, 0]
        first_bot_cells = bfs(field, first_bot_cell, 10)
        for i in first_bot_cells:
            field[i[0]][i[1]] = 1

        second_bot_cell = [field.size - 1, field.size - 1]
        second_bot_cells = bfs(field, second_bot_cell, 10)
        for i in second_bot_cells:
            field[i[0]][i[1]] = 2

        player1 = PlayerPosition({'cells': first_bot_cells, 'archers': [],
                                  'money': 12, 'strong_units': [],
                                  'defence_towers': [], 'villages': []})

        player2 = PlayerPosition({'cells': second_bot_cells, 'archers': [],
                                  'money': 12, 'strong_units': [],
                                  'defence_towers': [], 'villages': []})

        self.position = Position(player1, player2, field)

    def play(self):
        while len(self.position.white.cells) != 0 and len(self.position.black.cells) != 0:
            self.position.white.money += len(self.position.white.cells) - \
                                      len(self.position.white.archers) * 3 - \
                                      len(self.position.white.strong_units) * 7 + \
                                      len(self.position.white.villages) * 5 - \
                                      len(self.position.white.defence_towers) * 2

            self.position.black.money += len(self.position.black.cells) - \
                                         len(self.position.black.archers) * 3 - \
                                         len(self.position.black.strong_units) * 7 + \
                                         len(self.position.black.villages) * 5 - \
                                         len(self.position.black.defence_towers) * 2

            if self.position.white.money < 0:
                for i in self.position.white.archers:
                    self.position.field[i[0]][i[1]] = 1
                self.position.white.archers = set()
                for i in self.position.white.strong_units:
                    self.position.field[i[0]][i[1]] = 1
                self.position.white.strong_units = set()
                self.position.white.money = 0

            my_moves = self.first_bot.move(self.position, True)
            self.position.do_moves(my_moves, True)

            if self.position.black.money < 0:
                for i in self.position.black.archers:
                    self.position.field[i[0]][i[1]] = 2
                self.position.black.archers = set()
                for i in self.position.black.strong_units:
                    self.position.field[i[0]][i[1]] = 2
                self.position.black.strong_units = set()
                self.position.black.money = 0

            black_moves = self.second_bot.move(self.position, False)
            self.position.do_moves(black_moves, False)

        if len(self.position.white.cells) == 0:
            return False
        else:
            return True
