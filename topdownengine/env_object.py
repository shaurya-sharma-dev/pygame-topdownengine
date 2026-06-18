# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game

class EnvObject(GameObject):
    def __init__(
        self,
        headless: bool=False, 
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        *groups: Any
    ) -> None:
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        self.frame_size = frame_size
        self.current_animation = self.animation_paths.keys()[0]

        super().__init__(headless, *groups)

    def update(self, dt: float, game: Game) -> None:
        super().update(dt, game)