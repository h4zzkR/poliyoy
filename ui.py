import arcade
import arcade.gui
from arcade.gui import UIManager
from control import Command
from map.hexagonal_map import MapState


class PlaceEnityButton(arcade.gui.UIFlatButton):

    command = None
    map_state = MapState()

    def set_command(self, command: Command):
        self.command = command

    def __init__(self, *args, **kwargs):
        super(PlaceEnityButton, self).__init__(*args, **kwargs)

        self.set_style_attrs(
            font_color=arcade.color.WHITE,
            font_color_hover=arcade.color.WHITE,
            font_color_press=arcade.color.WHITE,
            bg_color=arcade.color.GRAY,
            bg_color_hover=(51, 139, 57),
            bg_color_press=(28, 71, 32),
            border_color=arcade.color.AERO_BLUE,
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )


    def on_click(self):
        """ Called when user lets off button """
        print("Click flat button.")
        self.command.execute()