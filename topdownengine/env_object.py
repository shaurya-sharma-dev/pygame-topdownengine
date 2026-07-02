# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game
import pygame as pg

class EnvObject(GameObject):
    CAUSES_COLLISIONS = True
    
    def __init__(
        self,
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        rel_hitboxes: list[pg.Rect]=[],
        *groups: Any
    ) -> None:
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        if frame_size is not None:
            self.frame_size = frame_size

        super().__init__(*groups)

        # EnvObject.rel_hitboxes are relative to the EnvObject.
        # Meanwhile, EnvObject.hitboxes are in world space.
        self.rel_hitboxes = rel_hitboxes