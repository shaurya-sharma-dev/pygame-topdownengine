import pygame as pg
import random
from .game_object import GameObject
from .game import Game

class Camera:
    """Class that represents the Camera.

    Attributes:
        real_position (pygame.Vector2): The position of the camera, excluding screenshake.
        screenshake_offset (pygame.Vector2): The current screenshake offset.
        focus_game_object (GameObject|None): The GameObject to center the camera on. If None, the Camera will not center on any GameObject.
        screenshake (dict[str,float]): Current screenshake dictionary.
        position (pygame.Vector2): The position of the camera, factoring screenshake.
    """
    def __init__(self, game: Game):
        "Initialize the camera."
        self.real_position = pg.Vector2()
        self.screenshake_offset = pg.Vector2()
        self.focus_game_object = None
        self.screenshake = {"duration": 0, "intensity": 0}
        self.game = game

    @property
    def position(self) -> pg.Vector2:
        "Get the position of the camera with screenshake."
        return self.real_position + (self.screenshake_offset if self.screenshake["duration"] > 0 else pg.Vector2())

    def update_screenshake(self, dt: float) -> None:
        """Update the screenshake offset.
        
        Args:
            dt (float): The deltatime
        """
        if self.screenshake["duration"] > 0:
            self.screenshake_offset = pg.Vector2(
                random.uniform(-self.screenshake["intensity"], self.screenshake["intensity"]),
                random.uniform(-self.screenshake["intensity"], self.screenshake["intensity"]),
            )
        self.screenshake["duration"] = max(0, self.screenshake["duration"] - (dt/1000)) # dt is in milliseconds

    def track_game_object(self, dt: float) -> None:
        """Tracks the `focus_game_object` by snapping instantly to it.
        
        Args:
            dt (float): The deltatime
        """
        self.real_position = pg.Vector2(self.focus_game_object.position) - pg.Vector2(
            self.game.screen.width / GameObject.SCALE / 2, 
            self.game.screen.height / GameObject.SCALE / 2
        )

    def handle_bounds(self) -> None:
        "Handle camera bounds."
        self.real_position.x = max(0, self.position.x)
        self.real_position.y = max(0, self.position.y)

    def update(self, dt: float) -> None:
        """Update the Camera.

        Args:
            dt (float): The deltatime.
        """        
        self.update_screenshake(dt)

        if self.focus_game_object:
            self.track_game_object(dt)
        
        # Bounds
        self.handle_bounds()

class SmoothTrackerCamera(Camera):
    "A subclass of Camera with smoother tracking logic."

    def track_game_object(self, dt: float):
        """Tracks the `focus_game_object` by smoothly moving to its position.
        
        Args:
            dt (float): The deltatime
        """
        target_position = pg.Vector2(self.focus_game_object.position) - pg.Vector2(
            self.game.screen.width / GameObject.SCALE / 2, 
            self.game.screen.height / GameObject.SCALE / 2
        )

        self.real_position += (target_position - self.real_position) * (dt / 1000) * 5