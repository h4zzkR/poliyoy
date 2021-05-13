from fractions import Fraction

class Position:
    white = None
    black = None
    field = None

class MockFraction:
    money_amount = 15
    tiles: dict # список клеток страны (в т.ч. построек на них) (координат на карте)
    # постройки можно ставить только на своей территории, а вот юнитов не обязательно
    units_pos: dict # список позиций юнитов страны
    fraction_id: int
    isBot: bool
    step_delta: int # число, прибавляемое на каждом шаге

    village_spawned_cnt = 1

    def __init__(self):
        pass

class PlayerStateTransmitter:
    cells = set()
    archers = set()
    money = 0
    strong_units = set()
    defence_towers = set()
    villages = set()
    spawned_villages = 0
    is_white = 0  # [0, 1]

    def __init__(self, fraction):
        self.is_white = fraction.isBot
        self.cells.update(set(fraction.tiles.keys()))
        self.money = fraction.money_amount

        for (pos, obj) in fraction.tiles.items():
            if obj.entity_id >= 0:
                if obj.entity_id == 2:
                    self.villages.add(pos)
                elif obj.entity_id == 3:
                    self.defence_towers.add(pos)
            self.cells.add(obj.position)

        for (pos, obj) in fraction.tiles.items():
            if obj.entity_id == 0:
                self.archers.add(pos)
            elif obj.entity_id == 1:
                self.strong_units.add(pos)

        self.spawned_villages = fraction.village_spawned_cnt

    def forward(self, obj):
        self.cells = obj.cells
        self.archers = obj.archers
        self.money = obj.money
        self.strong_units = obj.strong_units
        self.defence_towers = obj.defence_towers
        self.villages = obj.villages
        self.spawned_villages = obj.spawned_villages


class PlayerStateTransmitterHandler:
    def forward(self, fraction_bot, fraction_player):
        return [PlayerStateTransmitter(fraction_bot), PlayerStateTransmitter(fraction_player)]

    def backward(self, moves_list):
        return moves_list
