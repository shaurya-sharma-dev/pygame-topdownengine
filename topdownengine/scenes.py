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
        
        Args:
            dt (float): The deltatime.
        """
        for container in self.ui_containers:
            container.update(dt)

    def render(self):
        "Render the scene."
        for container in self.ui_containers:
            container.render(self.game.screen)
    
class GameplayScene(BaseScene):
    """A scene that updates and renders all `GameObject` instances.
        
    Attributes:
        global_alpha (int): The global alpha for lighting.
    """
    
    def __init__(self, game):
        """Initialize the GameplayScene.
        
        Args:
            game (Game): The game object to use.
        """
        super().__init__(game)
        self.global_alpha = 0
        self._light_filters = {}
    
    def get_light(self, radius: int):
        if not radius in self._light_filters: self._light_filters[radius] = self.create_light(radius)
        return self._light_filters[(radius)]

    def create_light(self, radius: int):
        surface = pg.Surface((max(radius * 2, 1), max(radius * 2, 1)), pg.SRCALPHA)
        for i in range(int(radius), 0, -1):
            alpha = 255 * (1 - i / radius)
            pg.draw.circle(surface, (0, 0, 0, alpha), (radius, radius), i)
        return surface

    def update(self, dt):
        """Update the GameplayScene.
        
        Args:
            dt (float): The deltatime.
        """
        super().update(dt)
        self.game.game_object_group.update(dt, self.game)

    def render(self):
        "Render the GameplayScene."
        overlay = pg.Surface(self.game.screen.size, pg.SRCALPHA)
        overlay.fill((0, 0, 0, self.global_alpha))

        for game_obj in sorted(self.game.game_object_group.sprites(), key=lambda g: g.draw_index):
            cr = game_obj.rect.move(-self.game.camera.position * game_obj.SCALE)
            self.game.screen.blit(game_obj.image, cr)
            if self.global_alpha > 0 and game_obj.light_radius > 0:
                scaled_lr = game_obj.light_radius * game_obj.SCALE
                overlay.blit(
                    self.get_light(
                        scaled_lr
                    ), 
                    (
                        cr.centerx - scaled_lr, 
                        cr.top
                    ), 
                    special_flags=pg.BLEND_RGBA_SUB
                )
        
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

        self.game.screen.blit(overlay, (0, 0))

        super().render() # Draw UI