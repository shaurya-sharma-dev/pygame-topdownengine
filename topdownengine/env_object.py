# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from .game_object import GameObject
from typing import Any
from .game import Game
import pygame as pg

class EnvObject(GameObject):
    """This class represents all environment objects in the engine.
    
    Attributes:
        CAUSES_COLLISIONS (bool): Overrides GameObject. Defaults to True.
    """
    CAUSES_COLLISIONS = True
    
    def __init__(
        self,
        animation_paths: dict[str,str]|None=None, 
        frame_size: tuple[int]|None=None, 
        colliders: list[pg.Rect]=None
    ) -> None:
        """Initialize the EnvObject.
        
        Args:
            animation_paths (dict[str,str], optional): The animation paths to load animations from. Defaults to None.
            frame_size (tuple[int]|None, optional): The frame size to use to load/generate animations. Defaults to None.
            colliders (list[pygame.Rect]|None, optional): The list of colliders of the EnvObject, relative to itself. If it is set to None, there will be no colliders. Defaults to None.
        """
        # Set animation paths dict and frame size before calling super().__init__()
        # This make it automatically load in the animations without
        # having to call it a second time.
        self.animation_paths = animation_paths
        if frame_size is not None:
            self.frame_size = frame_size

        super().__init__()
        self.colliders = colliders if colliders is not None else []