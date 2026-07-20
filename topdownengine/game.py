# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
from .scenes import GameplayScene, BaseScene

class Game:
    """Acts as the central core of the game and manages the core loop and gamestate.
    
    Attributes:
        screen (pygame.Surface): The primary display Surface.
        is_running (bool): Boolean flag to control execution.
        clock (pygame.time.Clock): Controls framerate and handles deltatime.
        fps (int): Integer that controls how much FPS the Game should have.
        game_object_group (GameObjectGroup): Stores all GameObjects.
        game_speed_percentage (float): The speed percentage for execution, ranging from `0` to `1`.
        debug (bool): If `True`, debug rendering will be enabled.
        target_scale (int): The target scale for the original window size.
        og_width (int): Original window width.
        extra_features (list[str]): List of extra features to add at runtime. You MUST set it during instantiation.
        camera (Camera): Camera object to use when rendering.
        bg_color (pygame.typing.ColorLike): Color to fill the screen with at the start of every draw cycle.
        scenes (dict[str, BaseScene]): Dictionary of all scene objects.
        active_scene_key (str): The dictionary key for the current active scene.
        active_scene (BaseScene): The active scene.
    """

    VALID_EXTRA_FEATURES = {"resize",}

    def __init__(
        self, 
        screen_width: int, 
        screen_height: int,
        window_title: str="pygame-topdownengine",
        window_icon_path: str|None=None,
        fps: int=60,
        debug: bool=False,
        target_scale: int=1,
        extra_features: list[str]=[]
    ) -> None:
        """Initialize the GameObject.
    
        Args:
            screen_width (int): The initial screen width.
            screen_height (int): The initial screen height.
            window_title (str): The window title. Defaults to "pygame-topdownengine".
            window_icon_path (str): The window icon path. Defaults to None.
            fps (int): Integer that controls how much FPS the Game should have.
            debug (bool): If `True`, debug rendering will be enabled. Defaults to False.
            target_scale (int): The target scale for the original window size. Defaults to 1.
            extra_features (list[str]): List of extra features to add at runtime. You MUST set it during instantiation. Defaults to [].
        """
        # Enabled features
        self.extra_features = extra_features
        for item in extra_features:
            if item not in self.VALID_EXTRA_FEATURES:
                raise ValueError(
                    f"'{item}' is not a valid extra feature and does nothing. "
                    f"Please choose from: {list(self.VALID_EXTRA_FEATURES)}"
                )

        # Initialize pygame-ce
        pg.init()

        # Initialize display
        if window_icon_path is not None:
            pg.display.set_icon(pg.image.load(window_icon_path))

        self.screen = pg.display.set_mode(
            (screen_width, screen_height), 
            pg.RESIZABLE if "resize" in extra_features else 0
        )
        pg.display.set_caption(window_title)
        self.og_width = screen_width

        # Clock + FPS
        self.clock = pg.time.Clock()
        self.fps = fps

        # Is Running Boolean Flag
        self.is_running = True

        # Debug Boolean Flag
        self.debug = debug

        # GameObject Group (Import Here to Prevent Circular Import)
        from .game_object import GameObjectGroup
        self.game_object_group = GameObjectGroup()

        # Game Speed Percentage
        self.game_speed_percentage = 1

        # Set Target Scale
        from .game_object import GameObject
        GameObject.set_scale(target_scale, self)

        # Camera (Import Here to Prevent Circular Import)
        from .camera import Camera
        self.camera = Camera()

        # Background Color
        self.bg_color = (255, 255, 255)

        # Scenes
        self.scenes = {
            "gameplay": GameplayScene(self)
        }
        self.active_scene_key = "gameplay"

        # Accumalated Deltatime
        self._accumulated_deltatime = 0

    @property
    def active_scene(self) -> BaseScene:
        "The active scene."
        return self.scenes[self.active_scene_key]

    def handle_events(self) -> None:
        "Handle events."
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                break
            elif event.type == pg.VIDEORESIZE:                
                # We import GameObject in handle_events to prevent a circular import.
                from .game_object import GameObject
                GameObject.set_scale(self.target_scale, self)
            self.active_scene.handle_event(event)

    def set_target_scale(self, target_scale: int) -> float:
        """Sets the target scale.
        
        Args:
            target_scale (int): The new target scale for the original screen dimensions.
        
        Returns:
            float: The new scale for the current window size.
        """
        self.target_scale = target_scale
        return self.target_scale * (self.screen.width / self.og_width)
    
    def update(self, dt: float) -> None:
        """Perform the update loop.
        
        Args:
            dt (float): The deltatime.
        """
        # Convert dt from milliseconds to seconds.
        dt = dt / 1000

        # Add a cap to one frame's dt to prevent infinite lag spirals
        if (dt > 0.25): dt = 0.25

        # Add processed dt to accumulater
        self._accumulated_deltatime += dt
        
        # Execute the update logic in steps of 1 / FPS
        while self._accumulated_deltatime >= 1 / self.fps:
            # Use 1000 / self.fps for update functions because
            # they still use milliseconds.
            self.active_scene.update(1000 / self.fps)
            self.camera.update(1000 / self.fps)

            # Subtract from accumulated deltatime in seconds.
            self._accumulated_deltatime -= 1 / self.fps

    def render(self) -> None:
        "Render everything to the screen."
        self.screen.fill(self.bg_color)
        self.active_scene.render()
        pg.display.flip()

    def run(self) -> None:
        "Run the game loop."
        while self.is_running:
            dt = self.clock.tick(self.fps) * self.game_speed_percentage
            self.handle_events()
            self.update(dt)
            self.render()
        pg.quit()
        exit()