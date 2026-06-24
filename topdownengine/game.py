# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
from .math import scale_rect

class Game:
    VALID_EXTRA_FEATURES = {'resize',}

    """Acts as the central core of the game and manages the core loop and gamestate.
    
    Attributes:
    - screen (pygame.Surface): The primary display Surface.
    - is_running (bool): Boolean flag to control execution.
    - clock (pygame.time.Clock): Controls framerate and handles deltatime.
    - fps (int): Integer that controls how much FPS the Game should have
    - game_object_group (pygame.sprite.Group): Stores all GameObjects.
    - game_speed_percentage (float): The speed percentage for execution, ranging from `0` to `1`.
    - debug (bool): If `True`, debug rendering will be enabled.
    - target_ratio (float): Target aspect ratio for resizing.
    - target_scale (int): The target scale for the original window size.
    - og_width (int): Original window width.
    - extra_features (list[str]): List of extra features to add at runtime. You MUST set it during instantiation.
    """

    def __init__(
        self, 
        screen_width: int, 
        screen_height: int,
        window_title: str='pygame-topdownengine',
        window_icon_path: str|None=None,
        fps: int=60,
        debug: bool=False,
        target_scale: int=1,
        extra_features: list[str]=[]
    ) -> None:
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
        self.target_ratio = screen_width/screen_height
        self.og_width = screen_width

        # Clock + FPS
        self.clock = pg.time.Clock()
        self.fps = fps

        # Is Running Boolean Flag
        self.is_running = True

        # Debug Boolean Flag
        self.debug = debug

        # GameObject Group
        self.game_object_group = pg.sprite.Group()

        # Game Speed Percentage
        self.game_speed_percentage = 1

        # Set Target Scale
        from .game_object import GameObject
        GameObject.set_scale(target_scale, self)

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                break
            elif event.type == pg.VIDEORESIZE:
                new_width = self.screen.width
                new_height = self.screen.height
                if new_width / new_height > self.target_ratio:
                    # Window is wider than the target aspect ratio
                    new_width = int(new_height * self.target_ratio)
                else:
                    # Window is taller than the target aspect ratio
                    new_height = int(new_width / self.target_ratio)
                
                # We import GameObject in handle_events to prevent a circular import.
                from .game_object import GameObject
                GameObject.set_scale(new_width / self.og_width * self.target_scale, self, True)
                self.screen = pg.display.set_mode((new_width, new_height), pg.RESIZABLE)
    
    def update(self, dt: float) -> None:
        self.game_object_group.update(dt, self)

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        for game_obj in sorted(self.game_object_group.sprites(), key=lambda g: g.draw_index):
            self.screen.blit(game_obj.image, game_obj.rect)
        # Draw debug in a separate loop so that it is drawn over images.
        if self.debug:
            for game_obj in self.game_object_group.sprites():
                # Draw Hitboxes
                for hitbox in game_obj.hitboxes:
                    pg.draw.rect(
                        self.screen, 
                        (0, 0, 255), 
                        scale_rect(hitbox, game_obj.SCALE),
                        1
                    )
        pg.display.flip()

    def run(self) -> None:
        while self.is_running:
            dt = self.clock.tick(self.fps) * self.game_speed_percentage
            self.handle_events()
            self.update(dt)
            self.render()
        pg.quit()
        exit()