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

    def move(self, mobile_obj: MobileObj, dt: float, dir: pg.Vector2) -> None:
        if dir.length() != 0: 
            dir.normalize_ip()
            dir *= self.speed

        dt_seconds = dt / 1000.0
        weight = 1.0 - math.exp(-self.snapping_speed * dt_seconds)
        mobile_obj.velocity = tde_math.lerp(mobile_obj.velocity, dir, weight)

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
        self.snapping_speed = 10.0

    def update(self, mobile_obj: MobileObj, dt: float) -> None:
        "Moves the MobileObj based on keyboard input."
        input = self.input_mgr.get_input()

        if 'Jump' in input:
            mobile_obj.jump()

        dir = pg.Vector2(
            int('Move Right' in input) - int('Move Left' in input),
            int('Move Down' in input) - int('Move Up' in input)
        )
        self.move(mobile_obj, dt, dir)

class MovementAIController(BaseMobileObjController):
    def __init__(self, target_mobile_obj: MobileObj) -> None:
        self.target_mobile_obj = target_mobile_obj
        self.speed = 1.5
        self.snapping_speed = 10.0

    def update(self, mobile_obj: MobileObj, dt: float) -> None:
        "Move the MobileObj towards the target."
        dir = self.target_mobile_obj.position - mobile_obj.position
        self.move(mobile_obj, dt, dir)