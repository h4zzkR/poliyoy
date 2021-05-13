from builders import EntityBuilder, EntityDirector
from config import OWNED_TILE_ID, OWNED_TILE_SALARY, ENTITIES_CONFIG, ENTITY_ID2COST, TREE_ID


class Fraction:
    money_amount = 15
    tiles: dict # список клеток страны (в т.ч. построек на них) (координат на карте)
    # постройки можно ставить только на своей территории, а вот юнитов не обязательно
    units_pos: dict # список позиций юнитов страны
    color: tuple          # цвет клеток страны
    fraction_id: int
    isBot: bool
    fraction_capital_pos: tuple
    step_delta: int # число, прибавляемое на каждом шаге

    village_spawned_cnt = 1
    village_cost = ENTITY_ID2COST[2]
    village_cost_prev = ENTITY_ID2COST[2]

    def __init__(self, color, fraction_id, isBot=False):
        self.color = color
        self.fraction_id = fraction_id
        self.isBot = isBot
        self.tiles = dict()
        self.units_pos = dict()
        self.fraction_capital_pos = ()
        self.step_delta = 1

        self.entity_director = EntityDirector()
        self.entity_director.builder = EntityBuilder()

    def build_tree(self, pos: tuple = None):
        self.entity_director.set_fraction(-1)
        entity = self.entity_director.build_entity(TREE_ID, pos).get()
        return entity

    def build_entity(self, entity_id: int, pos: tuple = None, no_update = False):
        # no_update - no update village cost
        self.entity_director.set_fraction(self.fraction_id)
        entity = self.entity_director.build_entity(entity_id, pos).get()

        if not no_update and entity_id == 2:
            if self.village_cost > self.money_amount:
                return None
            self.money_amount -= self.village_cost
            self.village_spawned_cnt += 1
            self.village_cost_prev = self.village_cost
            self.village_cost = ENTITIES_CONFIG["village"]["cost"] * self.village_spawned_cnt

        else:
            if entity.cost > self.money_amount:
                return None
            self.money_amount -= entity.cost

        self.tiles.update({pos: entity})
        if entity.move_range != 0:
            self.units_pos.update({pos : entity})

        self.step_delta -= entity.salary

        return entity

    def move_unit(self, old_pos, new_pos):
        unit = self.units_pos[old_pos]
        self.units_pos.update({new_pos : unit})

        if old_pos in self.units_pos.keys(): # переместились на собственную клетку
            del self.units_pos[old_pos]

    def detach_tile(self, pos):
        del self.tiles[pos]
        del self.units_pos[pos]
        self.step_delta += OWNED_TILE_SALARY

    def make_step(self):
        self.money_amount += self.step_delta
        if self.money_amount < 0 or len(self.tiles.keys()) == 0:
            return True
        return False

    def update_step_delta(self, delta):
        self.step_delta += delta

    def add_money(self, amount):
        self.money_amount += amount