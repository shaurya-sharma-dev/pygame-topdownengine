import pygame as pg
import random
from .game_object import GameObject

class Camera:
    """Class that represents the Camera.

    Attributes:
        real_position (pygame.Vector2): The position of the camera, excluding screenshake.
        screenshake_offset (pygame.Vector2): The current screenshake offset.
        focus_game_object (GameObject): The GameObject to center the camera on.
        screenshake (dict[str,float]): Current screenshake dictionary.
        position (pygame.Vector2): The position of the camera, factoring screenshake.
    """
    def __init__(self):
        "Initialize the camera."
        self.real_position = pg.Vector2()
        self.screenshake_offset = pg.Vector2()
        self.focus_game_object = None
        self.screenshake = {"duration": 0, "intensity": 0}

    @property
    def position(self) -> pg.Vector2:
        "Get the position of the camera with screenshake."
        return self.real_position + (self.screenshake_offset if self.screenshake["duration"] > 0 else pg.Vector2())

    def update(self, dt: float):
        """Update the Camera.

        Args:
            dt (float): The deltatime.
        """
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