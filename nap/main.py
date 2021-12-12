import arcade
from nap.views.map import MapView

class MapGame(arcade.Window):
    def __init__(self):
        super().__init__(500, 500, "Nap")
        self.map_view = MapView()

    def setup(self):
        self.map_view.setup()
        self.show_view(self.map_view)


def main():
    window = MapGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
