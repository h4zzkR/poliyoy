from __future__ import annotations
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

class SpawnEntity(Command):
    def __init__(self, receiver1, map_state, entity_id, update_state_command) -> None:
        self.entity_id = entity_id
        self.map_state = map_state
        self._receiver1 = receiver1 # map
        self._receiver2 = None
        self.update = update_state_command

    def execute(self) -> None:
        self._receiver2 = self.map_state.get_last_fraction()
        # print(self._receiver2.fraction_id)
        pos = self.map_state.last_mouse_tile_pos
        spawned = self._receiver1.spawn_entity(self.entity_id, self.map_state.last_mouse_tile_pos, self._receiver2)
        if spawned:
            self._receiver1.set_defence(pos)
            self.update.execute(self.entity_id)


class MoveUnit(Command):
    def __init__(self, receiver1, map_state, update_state_command) -> None:
        self.map = receiver1
        self.map_state = map_state
        self.fraction = None
        self.update = update_state_command

    def execute(self) -> None:
        self.fraction = self.map_state.get_last_fraction()
        old_pos = self.map_state.last_mouse_tile_pos
        new_pos = self.map_state.last_mouse_right_tile_pos
        # print(self.fraction.fraction_id)

        is_moved = self.map.move_unit(old_pos, new_pos)
        # print(is_moved, is_moved_on_own_tile)
        if is_moved:
            self.fraction.move_unit(old_pos, new_pos)
            self.map.set_defence(new_pos, old_pos)
            self.update.execute()


class UpdateGameState(Command):
    def __init__(self, game_window = None):
        self.game_window = game_window

    def execute(self, entity_id = None) -> None:
        if self.game_window:
            self.game_window.update_screen_info()
        if entity_id == 2: # village
            self.game_window.update_village_btn()


class NextStep(Command):
    def __init__(self, game_window):
        self.game_window = game_window

    def execute(self) -> None:
        self.game_window.on_next_step_key_press()