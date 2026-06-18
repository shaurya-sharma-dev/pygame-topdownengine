from .controls import KeyboardInputManager
import pygame as pg
import math
from topdownengine import math as tde_math

class BaseMobController:
    "A base class for all mob controllers."
    def update(self, mob, dt: float):
        """Update function for mob controllers."""
        pass

class KeyboardInputController(BaseMobController):
    def __init__(self):
        self.input_mgr = KeyboardInputManager()

    def update(self, mob, dt: float):
        input = self.input_mgr.get_input()
        # dir = pg.Vector2(pg.mouse.get_pos())/mob.SCALE - mob.position
        dir = pg.Vector2(
            int('Move Right' in input) - int('Move Left' in input),
            int('Move Down' in input) - int('Move Up' in input)
        )
        if dir.length() != 0: 
            dir.normalize_ip()
            dir *= 2

        dt_seconds = dt / 1000.0
        snapping_speed = 10.0
        weight = 1.0 - math.exp(-snapping_speed * dt_seconds)
        mob.velocity = tde_math.lerp(mob.velocity, dir, weight)

        if 'Jump' in input:
            mob.jump()