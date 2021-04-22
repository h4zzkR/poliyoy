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
        obj = self._receiver2.build_entity(self.entity_id, pos)
        self._receiver1.spawn_entity(obj, self.map_state.last_mouse_tile_pos)