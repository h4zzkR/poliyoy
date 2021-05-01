from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SpawnEntity(Command):
    def __init__(self, receiver1, map_state, entity_id) -> None:
        self.entity_id = entity_id
        self.map_state = map_state
        self._receiver1 = receiver1 # map
        self._receiver2 = None

    def execute(self) -> None:
        self._receiver2 = self.map_state.last_fraction
        pos = self.map_state.last_mouse_tile_pos
        spawned = self._receiver1.spawn_entity(self.entity_id, self.map_state.last_mouse_tile_pos, self._receiver2)
        if spawned:
            self._receiver1.set_defence(pos)
            # self.map_state.get_last_fraction().step_gold_delta()


class MoveUnit(Command):
    def __init__(self, receiver1, map_state) -> None:
        self.map = receiver1
        self.map_state = map_state
        self.fraction = None

    def execute(self) -> None:
        self.fraction = self.map_state.last_fraction
        old_pos = self.map_state.last_mouse_tile_pos
        new_pos = self.map_state.last_mouse_right_tile_pos

        is_moved, is_moved_on_own_tile = self.map.move_unit(old_pos, new_pos)
        # print(is_moved, is_moved_on_own_tile)
        if is_moved:
            self.fraction.move_unit(old_pos, new_pos, is_moved_on_own_tile)
            self.map.set_defence(new_pos, old_pos)