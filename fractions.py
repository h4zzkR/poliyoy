from builders import EntityBuilder, EntityDirector


class Fraction:
    money_amount = 100
    entities: dict # список зданий и юнитов страны (координат на карте)
    color: tuple          # цвет клеток страны
    fraction_id: int
    fraction_tiles: dict # словарь (или списко) номеров клеток страны
    isBot: bool
    fraction_capital_pos: tuple

    def __init__(self, color, fraction_id, isBot=False):
        self.color = color
        self.fraction_id = fraction_id
        self.isBot = isBot
        self.entities = {}
        self.fraction_capital_pos = ()

        self.entity_director = EntityDirector()
        self.entity_director.builder = EntityBuilder()

    def build_entity(self, entity_id: int, pos: tuple = None):
        self.entity_director.set_fraction(self.fraction_id)
        return self.entity_director.build_entity(entity_id, pos).get()
