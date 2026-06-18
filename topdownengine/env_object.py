# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game
import pygame as pg

class EnvObject(GameObject):
    def __init__(
        self,
        headless: bool=False, 
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        colliders: list[pg.Rect]=[],
        *groups: Any
    ) -> None:
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        self.frame_size = frame_size

        # Colliders are relative to the EnvObject.
        # Meanwhile, hitboxes are in world space.
        self.colliders = colliders

        super().__init__(headless, *groups)
        self.current_animation = self.animation_paths.keys()[0]

    @property
    def hitboxes(self) -> list[pg.Rect]:
        """Return a list of hitbox Rects in world-space, as opposed to
        EnvObject.colliders, which uses relative positioning to the
        EnvObject itself."""
        return [
            pg.Rect(c.left + self.position.x, c.top + self.position.y, c.width, c.height)
            for c in self.colliders
        ]

    def update(self, dt: float, game: Game) -> None:
        super().update(dt, game)