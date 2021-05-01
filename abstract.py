from abc import ABC, abstractmethod
from arcade import Sprite

class AbstractEntity(ABC):

    entity_id: int
    fraction_id: int
    damage: int
    health: int
    salary: int
    damage_range: int
    move_range: int
    position: (int, int)
    texture_scale: float
    cost_scale: int
    used_in_step: bool = False

    def attacked(self, hp : int):
        pass

    def hash(self):
        return hash(self)

    def attack_unit(self, unit):
        pass

    def possible_moves(self):
        """
        Возвращает список плиток, которые находятся в зоне доступности
        относительно move_range
        :return:
        """
        pass

    def set_param(self, param_dict : dict):
        '''
        :param param_dict: {param_name : param_value}
        :return:
        '''
        key = param_dict.keys()[0]
        self.__dict__[key] = param_dict[key]

    def move_to(self, pos):
        self.position = pos

    def __copy__(self):
        new_entity = self.__class__()
        new_entity.entity_id = self.entity_id
        new_entity.fraction_id = self.fraction_id
        new_entity.damage = self.damage
        new_entity.health = self.health
        new_entity.salary = self.salary
        new_entity.damage_range = self.damage_range
        new_entity.move_range = self.move_range
        new_entity.position = self.position
        new_entity.texture_scale = self.texture_scale
        new_entity.__dict__.update(self.__dict__)
        return new_entity

    def __deepcopy__(self, memo=None):
        if memo is None:
            memo = {}
        return self.__copy__()

    def __init__(self):
        pass


class AbstractUnit(AbstractEntity):
    def __init__(self, *args, **kwargs):
        super(AbstractUnit, self).__init__()

class AbstractBuilding(AbstractEntity):
    def __init__(self, *args, **kwargs):
        super(AbstractBuilding, self).__init__()
