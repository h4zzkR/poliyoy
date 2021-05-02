import arcade
import arcade.gui
from arcade.gui import UIManager
from control import Command

from control import SpawnEntity, NextStep, UpdateGameState, MoveUnit
from arcade.gui import UIFlatButton, UIManager
from config import ENTITY_ID2COST


class PlaceEntityButton(arcade.gui.UIFlatButton):
    command = None

    def set_command(self, command: Command):
        self.command = command

    def __init__(self, *args, **kwargs):
        super(PlaceEntityButton, self).__init__(*args, **kwargs)

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            font_size=15,
            bg_color=arcade.color.GRAY,
            bg_color_hover=(51, 139, 57),
            bg_color_press=(28, 71, 32),
            border_color=arcade.color.AERO_BLUE,
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE,
        )

    def on_click(self):
        """ Called when user lets off button """
        self.command.execute()


class NextStepButton(PlaceEntityButton):
    command = None

    def __init__(self, *args, **kwargs):
        super(NextStepButton, self).__init__(*args, **kwargs)

        self.set_style_attrs(
            bg_color = arcade.color.RED_DEVIL,
            bg_color_hover = arcade.color.ROSE_RED,
            bg_color_press = arcade.color.RED_BROWN,
            font_size=25,
        )

    def set_command(self, command: Command):
        self.command = command


def set_ui(game_obj):
    btn_w, btn_h = 50, 50
    
    next_btn = NextStepButton(text="Step", center_x=game_obj.w + 1.75 * game_obj.ui_margin_left,
                              center_y=game_obj.h - game_obj.ui_margin_top, width=btn_w * 2.1, height=btn_h)
    next_btn.set_command(NextStep(game_obj))
    game_obj.ui_manager.add_ui_element(next_btn)

    btn1 = PlaceEntityButton(text=f"V: {ENTITY_ID2COST[2]}", center_x=game_obj.w + game_obj.ui_margin_left,  # village
                             center_y=next_btn.center_y - 1.2 * btn_h, width=btn_w, height=btn_h, id="village")
    btn1.set_command(SpawnEntity(game_obj.map, game_obj.state, 2, UpdateGameState(game_obj)))
    game_obj.ui_manager.add_ui_element(btn1)

    btn2 = PlaceEntityButton(text=f"W: {ENTITY_ID2COST[1]}", center_x=btn1.center_x + btn_w * 1.2,
                             center_y=btn1.center_y, width=btn_w, height=btn_h, id="warrior")
    btn2.set_command(SpawnEntity(game_obj.map, game_obj.state, 1, UpdateGameState(game_obj)))
    game_obj.ui_manager.add_ui_element(btn2)

    btn3 = PlaceEntityButton(text=f"S: {ENTITY_ID2COST[0]}", center_x=btn1.center_x,
                             center_y=btn1.center_y - 1.2 * btn_h, width=btn_w, height=btn_h, id="scout")
    btn3.set_command(SpawnEntity(game_obj.map, game_obj.state, 0, UpdateGameState(game_obj)))
    game_obj.ui_manager.add_ui_element(btn3)

    btn4 = PlaceEntityButton(text=f"T: {ENTITY_ID2COST[3]}", center_x=btn2.center_x,
                             center_y=btn3.center_y, width=btn_w, height=btn_h, id="tower")
    btn4.set_command(SpawnEntity(game_obj.map, game_obj.state, 3, UpdateGameState(game_obj)))
    game_obj.ui_manager.add_ui_element(btn4)

    money_label = arcade.gui.UILabel(
        f'Gold: {game_obj.hosts[game_obj.gamer_host].money_amount}',
        center_x=btn3.center_x + btn_w * 0.55,
        center_y=btn3.center_y - btn_h,
        id="money_amount"
    )
    game_obj.ui_manager.add_ui_element(money_label)

    money_step = arcade.gui.UILabel(
        f'Delta: {game_obj.hosts[game_obj.gamer_host].step_delta}',
        center_x=money_label.center_x,
        center_y=money_label.center_y - btn_h * 0.65,
        id="money_step"
    )
    game_obj.ui_manager.add_ui_element(money_step)
    
def update_ui(game_obj):
    btn = game_obj.ui_manager.find_by_id("village")
    center_x, center_y, w, h, text = btn.center_x, btn.center_y, btn.width, btn.height, btn.text

    btn.remove_from_sprite_lists()
    del game_obj.ui_manager._id_cache["village"]  # sorry for that

    cost = game_obj.hosts[game_obj.gamer_host].village_cost
    btn = PlaceEntityButton(text=f"V: {cost}", center_x=center_x,  # village
                            center_y=center_y, width=w, height=h, id="village")
    btn.set_command(SpawnEntity(game_obj.map, game_obj.state, 2, UpdateGameState(game_obj)))
    game_obj.ui_manager.add_ui_element(btn)