from .controls import KeyboardInputManager
import pygame as pg
import math
from topdownengine import math as tde_math

class BaseMobController:
    "A base class for all mob controllers."
    def update(self, mob, dt: float):
        """Update function for mob controllers."""
        pass

class StaticController(BaseMobController):
    "A mob controller that keeps the mob still."
    def update(self, mob, dt):
        "Sets the mob's velocity to (0, 0)."
        mob.velocity = pg.Vector2()

class KeyboardInputController(BaseMobController):
    "A mob controller that uses keyboard inputs."
    def __init__(self):
        "Initializes the input manager."
        self.input_mgr = KeyboardInputManager()
        self.speed = 2

    def update(self, mob, dt: float):
        "Moves the mob based on keyboard input."
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
        mob.velocity = tde_math.lerp(mob.velocity, dir, weight)

        if 'Jump' in input:
            mob.jump()