import pygame as pg
import random
from .game_object import GameObject

class Camera:
    def __init__(self):
        self.real_position = pg.Vector2()
        self.screenshake_offset = pg.Vector2()
        self.focus_game_object = None
        self.screenshake = {"duration": 0, "intensity": 0}

    @property
    def position(self) -> pg.Vector2:
        return self.real_position + (self.screenshake_offset if self.screenshake["duration"] > 0 else pg.Vector2())

    def update(self, dt: float):
        if self.screenshake["duration"] > 0:
            self.screenshake_offset = pg.Vector2(
                random.uniform(-self.screenshake["intensity"], self.screenshake["intensity"]),
                random.uniform(-self.screenshake["intensity"], self.screenshake["intensity"]),
            )
        self.screenshake["duration"] = max(0, self.screenshake["duration"] - (dt/1000)) # dt is in milliseconds
        
        if self.focus_game_object:
            screen = pg.display.get_surface()
            self.real_position = pg.Vector2(self.focus_game_object.position) - pg.Vector2(
                screen.width / GameObject.SCALE / 2, 
                screen.height / GameObject.SCALE / 2
            )
        
        # Bounds
        self.real_position.x = max(0, self.position.x)
        self.real_position.y = max(0, self.position.y)