# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from topdownengine.controls import KeyboardInputManager
import pygame as pg
import math
from topdownengine import math as tde_math
from . import MobileObject

class BaseController:
    "A base class for all MobileObj controllers."
    def update(self, mobile_obj: MobileObject, dt: float) -> None:
        """Update function for MobileObj controllers."""
        pass

    def move(self, mobile_object: MobileObject, dt: float, dir: pg.Vector2) -> None:
        """Change a MobileObj's velocity using a given dir Vector.
        
        Args:
            mobile_obj (MobileObj): The MobileObj to move
            dt (float): The deltatime
            dir (pg.Vector2): Vector to move by
        """
        if dir.length() != 0: 
            dir.normalize_ip()
            dir *= self.speed

        dt_seconds = dt / 1000.0
        weight = 1.0 - math.exp(-self.snapping_speed * dt_seconds)
        mobile_object.velocity = tde_math.lerp(mobile_object.velocity, dir, weight)

class StaticController(BaseController):
    "A MobileObj controller that keeps the MobileObj still."
    def update(self, mobile_object: MobileObject, dt: float) -> None:
        "Sets the MobileObj's velocity to (0, 0)."
        mobile_object.velocity = pg.Vector2()

class KeyboardInputController(BaseController):
    "A MobileObj controller that uses keyboard inputs."
    def __init__(self) -> None:
        "Initializes the input manager."
        self.input_mgr = KeyboardInputManager()
        self.speed = 2
        self.snapping_speed = 10.0

    def update(self, mobile_object: MobileObject, dt: float) -> None:
        "Moves the MobileObj based on keyboard input."
        input = self.input_mgr.get_input()

        if 'Jump' in input:
            mobile_object.jump()

        dir = pg.Vector2(
            int('Move Right' in input) - int('Move Left' in input),
            int('Move Down' in input) - int('Move Up' in input)
        )
        self.move(mobile_object, dt, dir)

class MovementAIController(BaseController):
    def __init__(self, target_mobile_object: MobileObject) -> None:
        self.target_mobile_object = target_mobile_object
        self.speed = 1.5
        self.snapping_speed = 10.0

    def update(self, mobile_object: MobileObject, dt: float) -> None:
        "Move the MobileObj towards the target."
        dir = self.target_mobile_object.position - mobile_object.position
        self.move(mobile_object, dt, dir)