class HexagonalField(list):
    size = 15

    def __init__(self):
        super().__init__()
        for i in range(self.size):
            self.append([0] * self.size)

    def get_neighbour(self, x, y) -> list:
        answer = []
        candidates = [(x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y)]
        if x % 2 == 0:
            candidates.append((x + 1, y + 1))
            candidates.append((x - 1, y + 1))
        else:
            candidates.append((x + 1, y - 1))
            candidates.append((x - 1, y - 1))

        for i in candidates:
            if 0 <= i[0] < self.size and 0 <= i[1] < self.size:
                answer.append(i)
        return answer


class PlayerPosition:
    cells = set()
    archers = set()
    money = 0
    strong_units = set()
    defence_towers = set()
    villages = set()

    def __init__(self, params):
        if params:
            self.cells = params['cells'].copy()
            self.archers = params['archers'].copy()
            self.money = params['money']
            self.strong_units = params['strong_units'].copy()
            self.defence_towers = params['defence_towers'].copy()
            self.villages = params['villages'].copy()

    def copy(self, pos):
        self.cells = pos.cells
        self.villages = pos.villages
        self.strong_units = pos.strong_units
        self.defence_towers = pos.defence_towers
        self.money = pos.money
        self.archers = pos.archers


class Position:
    white = PlayerPosition(None)
    black = PlayerPosition(None)
    field = HexagonalField()

    def __init__(self, white: PlayerPosition,
                 black: PlayerPosition,
                 field: HexagonalField):
        self.white = white
        self.black = black
        self.field = field

    def do_moves(self, moves, is_white):
        for i in moves:
            if i['command'] == 'create_village':
                if is_white:
                    self.white.money -= 12 + 2 * len(self.white.villages)
                    self.field[i[1][0]][i[1][1]] = 9
                    self.white.villages.add((i[1][0], i[1][1]))
                else:
                    self.black.money -= 12 + 2 * len(self.black.villages)
                    self.field[i[1][0]][i[1][1]] = 10
                    self.black.villages.add((i[1][0], i[1][1]))
            elif i['command'] == 'create_archer':
                if is_white:
                    self.white.money -= 3
                    self.field[i[1][0]][i[1][1]] = 3
                    self.white.archers.add((i[1][0], i[1][1]))
                else:
                    self.black.money -= 3
                    self.field[i[1][0]][i[1][1]] = 4
                    self.black.archers.add((i[1][0], i[1][1]))
            elif i['command'] == 'create_strong_unit':
                if is_white:
                    self.white.money -= 7
                    self.field[i[1][0]][i[1][1]] = 5
                    self.white.strong_units.add((i[1][0], i[1][1]))
                else:
                    self.black.money -= 7
                    self.field[i[1][0]][i[1][1]] = 6
                    self.black.strong_units.add((i[1][0], i[1][1]))
            elif i['command'] == 'create_defence_tower':
                if is_white:
                    self.white.money -= 15
                    self.field[i[1][0]][i[1][1]] = 7
                    self.white.defence_towers.add((i[1][0], i[1][1]))
                else:
                    self.black.money -= 15
                    self.field[i[1][0]][i[1][1]] = 8
                    self.black.defence_towers.add((i[1][0], i[1][1]))
            elif i['command'] == 'move_archer':
                if is_white:
                    self.field[i[1][0]][i[1][1]] = 1
                    self.field[i[2][0]][i[2][1]] = 3
                    self.white.cells.add((i[2][0], i[2][1]))
                    self.white.archers.remove((i[1][0], i[1][1]))
                    self.white.archers.add((i[2][0], i[2][1]))
                else:
                    self.field[i[1][0]][i[1][1]] = 2
                    self.field[i[2][0]][i[2][1]] = 4
                    self.black.cells.add((i[2][0], i[2][1]))
                    self.black.archers.remove((i[1][0], i[1][1]))
                    self.black.archers.add((i[2][0], i[2][1]))
            elif i['command'] == 'move_strong_unit':
                if is_white:
                    self.field[i[1][0]][i[1][1]] = 1
                    self.field[i[2][0]][i[2][1]] = 5
                    self.white.cells.add((i[2][0], i[2][1]))
                    self.white.strong_units.remove((i[1][0], i[1][1]))
                    self.white.strong_units.add((i[2][0], i[2][1]))
                else:
                    self.field[i[1][0]][i[1][1]] = 2
                    self.field[i[2][0]][i[2][1]] = 6
                    self.black.cells.add((i[2][0], i[2][1]))
                    self.black.strong_units.remove((i[1][0], i[1][1]))
                    self.black.strong_units.add((i[2][0], i[2][1]))