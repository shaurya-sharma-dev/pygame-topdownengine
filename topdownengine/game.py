# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg

class Game:
    """Acts as the central core of the game and manages the core loop and gamestate.
    
    This class initializes pygame-ce, updates and renders all GameObjects,
    manages different states and transitions between them, runs the core
    gameplay loop, and serves as the root component.
    
    Attributes:
    - screen (pygame.Surface): The primary display Surface.
    - is_running (bool): Boolean flag to control execution.
    - clock (pygame.time.Clock): Controls framerate and handles deltatime.
    - fps (int): Integer that controls how much FPS the Game should have
    - game_object_group (pygame.sprite.Group): Stores all GameObjects.
    """

    def __init__(
        self, 
        screen_width: int, 
        screen_height: int,
        window_title: str='pygame-topdownengine',
        window_icon_path: str|None=None,
        fps: int=60
    ) -> None:
        # Initialize pygame-ce
        pg.init()

        # Initialize display
        if window_icon_path is not None:
            pg.display.set_icon(pg.image.load(window_icon_path))

        self.screen = pg.display.set_mode((screen_width, screen_height))
        pg.display.set_caption(window_title)

        # Clock + FPS
        self.clock = pg.time.Clock()
        self.fps = fps

        # Is Running Boolean Flag
        self.is_running = True

        # GameObject Group
        self.game_object_group = pg.sprite.Group()

    def handle_events(self) -> None:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
                break
    
    def update(self, dt: float) -> None:
        self.game_object_group.update(dt)

    def render(self) -> None:
        self.screen.fill((255, 255, 255))
        self.game_object_group.draw(self.screen)
        pg.display.flip()

    def run(self) -> None:
        while self.is_running:
            dt = self.clock.tick(self.fps)
            self.handle_events()
            self.update(dt)
            self.render()