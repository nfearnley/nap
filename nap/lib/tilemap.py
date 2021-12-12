from __future__ import annotations

import json
from pathlib import Path

from arcade import Sprite, SpriteList, Texture
import arcade

SCALE = 3


class TileMap:
    def __init__(
        self,
        mapfile: MapFile,
        tile_textures: list[Texture],
        bg_texture: Texture
    ):
        self.mapfile = mapfile
        bg_w, bg_h = bg_texture.size
        bg_w, bg_h = bg_w * SCALE, bg_h * SCALE
        grid_w, grid_h = mapfile.grid_size
        grid_w, grid_h = grid_w * SCALE, grid_h * SCALE
        grid_x, grid_y = mapfile.grid_offset
        grid_x, grid_y = grid_x * SCALE, grid_y * SCALE
        toolbar_h = grid_h * 4
        toolbar_w = grid_w * 4
        w, h = bg_w, bg_h + toolbar_h

        self.grid_w, self.grid_h = grid_w, grid_h
        self.grid_x, self.grid_y = grid_x, grid_y
        self.w, self.h = w, h
        self.tile_textures = tile_textures
        self.tiles: dict[tuple[int, int], tuple[int, Sprite]] = dict()
        self.sprites = SpriteList()

        bg_sprite = Sprite(texture=bg_texture)
        bg_sprite.scale = SCALE
        bg_sprite.left = 0
        bg_sprite.bottom = toolbar_h
        self.sprites.append(bg_sprite)

        toolbar_x = (self.w / 2) - (len(tile_textures) * toolbar_w // 2)
        for n, t in enumerate(tile_textures):
            print(t)
            toolbar_sprite = Sprite(texture=t)
            toolbar_sprite.scale = SCALE * 4
            toolbar_sprite.left = toolbar_x + (n * toolbar_w)
            toolbar_sprite.bottom = 0
            self.sprites.append(toolbar_sprite)

        for (x, y), tilenum in mapfile.tilemap:
            self[x, y] = tilenum

    def __getitem__(self, pos: tuple[int, int]):
        tilenum, _ = self.tiles[pos]
        return tilenum

    def __setitem__(self, pos: tuple[int, int], tilenum: int):
        if tilenum is None:
            del self[pos]
            return

        try:
            texture = self.tile_textures[tilenum]
        except (IndexError, TypeError):
            raise ValueError("Invalid tile number")

        if pos in self.tiles:
            old_tilenum, sprite = self.tiles[pos]
            if tilenum == old_tilenum:
                return
        else:
            sprite = Sprite(
                image_width=self.grid_w,
                image_height=self.grid_h,
                texture=texture
            )
            sprite.left = self.grid_w * pos[0]
            sprite.top = self.grid_h * pos[1]
            self.sprites.append(sprite)

        sprite.texture = texture
        self.tiles[pos] = tilenum, sprite

    def __delitem__(self, pos: tuple[int, int]):
        if pos not in self.tiles:
            raise KeyError(pos)
        _, sprite = self.tiles[pos]
        self.sprites.remove(sprite)
        del self.tiles[pos]

    def draw(self):
        self.sprites.draw(pixelated=True)

    @classmethod
    def load(cls, path: Path):
        mapfile = MapFile.load(path)
        bg_texture = mapfile.load_bg_texture()
        tile_textures = mapfile.load_tile_textures()
        return TileMap(mapfile, tile_textures, bg_texture)

    def save(self):
        self.mapfile.tilemap = [[[x, y], tilenum] for (x, y), (tilenum, _) in self.tiles.items()]
        self.mapfile.save()


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
