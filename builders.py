from abc import ABC, abstractmethod

from abstract import AbstractEntity
from config import *
from entity import *
from fractions import FractionType


class EntityBuilder(ABC):
    entity: AbstractEntity

    def __init__(self):
        self.reset()

    def reset(self):
        self.entity = AbstractBuilding()

    def get(self) -> AbstractEntity:
        entity = self.entity
        self.reset()
        return entity

    def set_fraction(self, fraction_id):
        self.entity.fraction_id = fraction_id

    def set_parameter(self, param: dict):
        """
        Обновить характеристику
        :param param: { param_name : param_value }
        :return:
        """
        self.entity.__dict__[param[0]] = param[1]

    @abstractmethod
    def set_position(self, position: (int, int)) -> None:
        pass

    def set_entity_type(self, entity_type_id):
        self.entity.entity_id = entity_type_id
        self.entity.__class__ = TypeInfo.id2type[entity_type_id]


class EntityDirector(ABC):
    _builder: EntityBuilder

    def __init__(self):
        pass

    @property
    def builder(self):
        self._builder = None

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def apply_modifiers(self, config: dict):
        """
        У фракций есть определенные 'способности',
        так у одной фракции может быть дополнительный урон юнитов,
        у другой - больше здоровья для юнитов. Этот метод применяет модификаторы
        характеристик к объекту
        :param config:
        :return:
        """
        for item in config.items():
            self._builder.entity.__dict__[item[0]] *= item[1]

    def fraction(self, fraction_id):
        """
        Задать фракцию произвольного объекта
        :param fraction_type:
        :return:
        """
        self.apply_modifiers(ENTITIES_CONFIG[f"fraction{fraction_id}_modifiers"])

    def fraction0(self):
        self.apply_modifiers(ENTITIES_CONFIG["fraction0_modifiers"])
        self._builder.set_fraction(0)
        return self

    def fraction1(self):
        self.apply_modifiers(ENTITIES_CONFIG["fraction1_modifiers"])
        self._builder.set_fraction(1)
        return self

    def build_entity(self, entity_type_id, position):
        typename = TypeInfo.id2typename.get(entity_type_id)
        for item in ENTITIES_CONFIG[typename].items():
            self._builder.set_parameter(item)
        self._builder.set_entity_type(ENTITIES_CONFIG[typename]["type_id"])
        self._builder.set_position(position)
        return self

    def get(self):
        return self._builder.get()


class UnitBuilder(EntityBuilder):
    entity = AbstractEntity

    def __init__(self):
        super(UnitBuilder, self).__init__()

    def set_position(self, position):
        self.entity.position = position


class BuildingBuilder(EntityBuilder):
    entity = AbstractEntity

    def set_position(self, position):
        self.entity.position = position


class UnitDirector(EntityDirector):

    def __init__(self):
        super(UnitDirector, self).__init__()

    def build_archer(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["archer"], position)
        return self

    def build_swordsman(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["swordsman"], position)
        return self


class BuildingsDirector(EntityDirector):

    def __init__(self):
        super(BuildingsDirector, self).__init__()

    def build_village(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["village"], position)
        return self

    def build_defence_tower(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["defencetower"], position)
        return self


if __name__ == "__main__":
    director1 = UnitDirector()
    director1.builder = UnitBuilder()
    director1._builder = UnitBuilder()
    archer = director1.build_archer().fraction0().get()
    swordsman = director1.build_swordsman().fraction1().get()

    director2 = BuildingsDirector()
    director2._builder = BuildingBuilder()
    village = director2.build_village().fraction1().get()
    print(village)
