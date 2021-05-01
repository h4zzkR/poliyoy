import arcade
import arcade.gui
from arcade.gui import UIManager
from control import Command
from game_state import GameState


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
