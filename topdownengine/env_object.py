# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game
import pygame as pg

class EnvObject(GameObject):
    def __init__(
        self,
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        colliders: list[pg.Rect]=[],
        *groups: Any
    ) -> None:
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        if frame_size is not None:
            self.frame_size = frame_size

        super().__init__(*groups)

        # Colliders are relative to the EnvObject.
        # Meanwhile, hitboxes are in world space.
        self.colliders = colliders

    def update(self, dt: float, game: Game) -> None:
        super().update(dt, game)