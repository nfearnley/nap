from pathlib import Path
import arcade

from nap.lib.tilemap import TileMap


class MapView(arcade.View):
    def __init__(self):
        super().__init__()
        self.tilemap = None

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()
        self.tilemap.draw()
        #arcade.draw_text("Map", 0, 0, arcade.color.DUKE_BLUE, 96, bold=True)

    def on_key_press(self, symbol: int, modifiers: int):
        super().on_key_press(symbol, modifiers)

        if symbol == arcade.key.ESCAPE:
            self.window.menu_view.setup()
            self.window.show_view(self.window.menu_view)

    def setup(self):
        self.tilemap = TileMap.load(Path("../nap-castlevania/map.json"))
        self.window.set_size(self.tilemap.w, self.tilemap.h)
