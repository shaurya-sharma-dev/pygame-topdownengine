import pygame as pg
from .math import scale_rect

class BaseScene:
    """A scene that determines the behavior of the game loop.
        
    Attributes:
        game (Game): The game object to use.
        ui_containers (list[UIContainer]): The list of UIContainers for this scene.
    """
    def __init__(self, game):
        """Initialize the scene.
        
        Args:
            game (Game): The game object to use.
        """
        self.game = game
        self.ui_containers = []

    def handle_event(self, event: pg.Event):
        """Handle a single event.
        
        Args:
            event (pygame.Event): The event to handle.
        """
        for container in self.ui_containers:
            container.handle_event(event)
    
    def update(self, dt: float):
        """Update the scene.
        
        Attributes:
            dt (float): The deltatime.
        """
        for container in self.ui_containers:
            container.update(dt)

    def render(self):
        "Render the scene."
        for container in self.ui_containers:
            container.render(self.game.screen)
    
class GameplayScene(BaseScene):
    def update(self, dt):
        """Update the GameplayScene.
        
        Attributes:
            dt (float): The deltatime.
        """
        super().update(dt)
        self.game.game_object_group.update(dt, self.game)

    def render(self):
        "Render the GameplayScene."
        super().render()
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
                        scale_rect(collider.move(-self.game.camera.position), game_obj.SCALE),
                        1
                    )