import pygame as pg
from .math import scale_rect
from .ui import UIContainer

class BaseScene:
    def __init__(self, game):
        self.game = game
        self._ui_containers = []

    @property
    def ui_containers(self) -> list[UIContainer]:
        return self._ui_containers
    
    @ui_containers.setter
    def ui_containers(self, new_containers: list[UIContainer]):
        self._ui_containers = new_containers

    def handle_event(self, event: pg.Event):
        for container in self.ui_containers:
            container.handle_event(event)
    
    def update(self, dt: float):
        for container in self.ui_containers:
            container.update(dt)

    def render(self):
        for container in self.ui_containers:
            container.render(self.game.screen)
    
class GameplayScene(BaseScene):
    def update(self, dt):
        super().update(dt)
        self.game.game_object_group.update(dt, self.game)

    def render(self):
        super().render()
        for game_obj in sorted(self.game.game_object_group.sprites(), key=lambda g: g.draw_index):
            self.game.screen.blit(game_obj.image, game_obj.rect.move(-self.game.camera.position * game_obj.SCALE))
        
        # Draw debug in a separate loop so that it is drawn over images.
        if self.game.debug:
            for game_obj in self.game.game_object_group.sprites():
                # Draw Hitboxes
                for hitbox in game_obj.hitboxes:
                    pg.draw.rect(
                        self.game.screen, 
                        (0, 0, 255), 
                        scale_rect(hitbox.move(-self.game.camera.position), game_obj.SCALE),
                        1
                    )