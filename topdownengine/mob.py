# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game

class Mob(GameObject):
    def __init__(
        self, 
        controller: Any, 
        headless: bool=False, 
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        directional_anims: bool=False, 
        *groups: Any
    ) -> None:
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        if frame_size is not None:
            self.frame_size = frame_size
        self.directional_anims = directional_anims
        if self.directional_anims:
            self.current_dir = 'd'

        super().__init__(headless, *groups)
        self.current_animation = self.animation_paths.keys()[0]
        self.controller = controller
        self.jump_vel = 0.75

    def update(self, dt: float, game: Game) -> None:
        self.controller.update(self, dt)
        super().update(dt, game)
        if self.velocity.length():
            self.current_animation = 'walk'
            angle = self.velocity.as_polar()[1]
            if -45 <= angle <= 45: # Right
                self.current_dir = 'r'

            elif (-180 <= angle <= -135) or (135 <= angle <= 180): # Left
                self.current_dir = 'l'

            elif 45 <= angle <= 135: # Down
                self.current_dir = 'd'

            elif -135 <= angle <= -45: # Up
                self.current_dir = 'u'
        else:
            self.current_animation = 'idle'

    def jump(self) -> None:
        if self.elevation == self.z:
            self.z_vel = self.jump_vel