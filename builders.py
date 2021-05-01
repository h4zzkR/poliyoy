from abc import ABC, abstractmethod

from abstract import AbstractEntity
from config import *
from entity import *


class AbstractEntityBuilder(ABC):
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

    def set_position(self, position: (int, int)) -> None:
        self.entity.position = position

    def set_entity_type(self, entity_type_id):
        self.entity.entity_id = entity_type_id
        self.entity.__class__ = TypeInfo.id2type[entity_type_id]

class AbstractEntityDirector(ABC):
    _builder: AbstractEntityBuilder

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
            # print(self._builder.entity)
            self._builder.entity.__dict__[item[0]] *= item[1]

    def set_fraction(self, fraction_id):
        """
        Задать фракцию произвольного объекта
        :param fraction_type:
        :return:
        """
        self._builder.set_fraction(fraction_id)
        return self

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
        try:
            if self._builder.entity.entity_id >= 0:
                self.apply_modifiers(ENTITIES_CONFIG[f"fraction{self._builder.entity.fraction_id}_modifiers"])
        except Exception:
            raise AttributeError("You must set fraction id")
        return self

    def get(self):
        return self._builder.get()
    
class EntityBuilder(AbstractEntityBuilder):
    
    def __init__(self):
        super(EntityBuilder, self).__init__()
        
    def set_position(self, position):
        self.entity.position = position

class EntityDirector(AbstractEntityDirector):

    def __init__(self):
        super(EntityDirector, self).__init__()

    def build_archer(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["archer"], position)
        return self

    def build_swordsman(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["swordsman"], position)
        return self

    def build_village(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["village"], position)
        return self

    def build_defence_tower(self, position=(None, None)):
        self.build_entity(TypeInfo.typename2id["defencetower"], position)
        return self


if __name__ == "__main__":
    pass
    # director1 = UnitDirector()
    # director1.builder = UnitBuilder()
    # director1._builder = UnitBuilder()
    # archer = director1.build_archer().fraction0().get()
    # swordsman = director1.build_swordsman().fraction1().get()
    # 
    # director2 = BuildingsDirector()
    # director2._builder = BuildingBuilder()
    # village = director2.build_village().fraction1().get()
    # print(village.hash(), swordsman.hash())
