import pygame as pg
from .math import scale_rect

class BaseScene:
    def __init__(self, game):
        self.game = game
    
    def update(self, dt: float):
        pass

    def render(self):
        pass
    
class GameplayScene(BaseScene):
    def update(self, dt):
        self.game.game_object_group.update(dt, self.game)

    def render(self):
        for game_obj in sorted(self.game.game_object_group.sprites(), key=lambda g: g.draw_index):
            self.game.screen.blit(game_obj.image, game_obj.rect.move(-self.game.camera.position * game_obj.SCALE))
        
        # Draw debug in a separate loop so that it is drawn over images.
        if self.game.debug:
            for game_obj in self.game.game_object_group.sprites():
                # Draw Colliders
                for collider in game_obj.world_colliders:
                    pg.draw.rect(
                        self.game.screen, 
                        (0, 0, 255), 
                        scale_rect(collider, game_obj.SCALE),
                        1
                    )