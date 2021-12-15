from __future__ import annotations

import json
from pathlib import Path

import arcade

SCALE = 3


class MapFile:
    def __init__(
        self,
        path: Path,
        grid_size: tuple[int, int],
        grid_offset: tuple[int, int],
        bg: str,
        tiles: str,
        tilemap: tuple[tuple[int, int], int]
    ):
        self.path = path
        self.bg = bg
        self.tiles = tiles
        self.grid_size = grid_size
        self.grid_offset = grid_offset
        self.tilemap = tilemap

    @classmethod
    def load(cls, path: Path):
        with path.open("r") as f:
            j = json.load(f)
        return MapFile(
            path,
            j["grid_size"],
            j.get("grid_offset", (0, 0)),
            j["bg"],
            j["tiles"],
            j.get("tilemap", [])
        )

    def load_bg_texture(self):
        root = self.path.parent
        return arcade.load_texture(root / self.bg)

    def load_tile_textures(self):
        root = self.path.parent
        return [arcade.load_texture(root / t) for t in self.tiles]

    def save(self):
        j = {
            "grid_size": self.grid_size,
            "grid_offset": self.grid_offset,
            "bg": self.bg,
            "tiles": self.tiles,
            "tilemap": self.tilemap
        }
        with self.path.open("w") as f:
            json.dump(j, f, indent=4)
