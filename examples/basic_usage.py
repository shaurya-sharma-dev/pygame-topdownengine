import topdownengine as tde
from topdownengine.mobile_obj.controller import KeyboardInputController
from topdownengine.asset_paths import ASSETS_DIR
import pygame as pg

# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a MobileObj
mobile_obj = tde.MobileObj(
    controller=KeyboardInputController(), 
    animation_paths={
        'idle': ASSETS_DIR / 'example-player' / 'idle.png',
        'walk': ASSETS_DIR / 'example-player' / 'walk.png'
    },
    frame_size=(16, 16),
    directional_anims=True
)

# Define an env_obj
env_obj = tde.EnvObject(colliders=[pg.Rect(0, 0, 16, 16)])
env_obj.position = pg.Vector2(100, 100)

# Add them both to the game object group
game.game_object_group.add(mobile_obj)
game.game_object_group.add(env_obj)

# Rescale GameObjects to have a SCALE of 3 (this makes them more visible)
tde.GameObject.set_scale(3, game)

# You can add subpixel rendering by uncommenting the below line of code
# tde.GameObject.SUBPIXEL = True

# Run the game
game.run()