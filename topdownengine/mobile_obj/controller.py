# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from topdownengine.controls import KeyboardInputManager
import pygame as pg
import math
from topdownengine import math as tde_math
from . import MobileObj

class BaseMobileObjController:
    "A base class for all MobileObj controllers."
    def update(self, mobile_obj: MobileObj, dt: float) -> None:
        """Update function for MobileObj controllers."""
        pass

class StaticController(BaseMobileObjController):
    "A MobileObj controller that keeps the MobileObj still."
    def update(self, mobile_obj: MobileObj, dt: float) -> None:
        "Sets the MobileObj's velocity to (0, 0)."
        mobile_obj.velocity = pg.Vector2()

class KeyboardInputController(BaseMobileObjController):
    "A MobileObj controller that uses keyboard inputs."
    def __init__(self) -> None:
        "Initializes the input manager."
        self.input_mgr = KeyboardInputManager()
        self.speed = 2

    def update(self, mobile_obj: MobileObj, dt: float) -> None:
        "Moves the MobileObj based on keyboard input."
        input = self.input_mgr.get_input()
        dir = pg.Vector2(
            int('Move Right' in input) - int('Move Left' in input),
            int('Move Down' in input) - int('Move Up' in input)
        )
        if dir.length() != 0: 
            dir.normalize_ip()
            dir *= self.speed

        dt_seconds = dt / 1000.0
        snapping_speed = 10.0
        weight = 1.0 - math.exp(-snapping_speed * dt_seconds)
        mobile_obj.velocity = tde_math.lerp(mobile_obj.velocity, dir, weight)

        if 'Jump' in input:
            mobile_obj.jump()