import topdownengine as tde
from topdownengine.mobile_object.controller import KeyboardInputController, MovementAIController
from topdownengine.asset_paths import ASSETS_DIR
import pygame as pg

# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a MobileObject to be the Player
player = tde.MobileObject(
    controller=KeyboardInputController(), 
    animation_paths={
        'idle': ASSETS_DIR / 'example-player' / 'idle.png',
        'walk': ASSETS_DIR / 'example-player' / 'walk.png'
    }, frame_size=(16, 16), directional_anims=True
)

# Define a MobileObject to follow the Player
enemy = tde.MobileObject(
    controller=MovementAIController(target_mobile_object=player), 
    animation_paths=player.animation_paths, # Use same animations as the Player
    frame_size=(16, 16), directional_anims=True
)

# Define an EnvObject
env_obj = tde.EnvObject(frame_size=(32, 32), colliders=[pg.Rect(0, 0, 32, 32)])
env_obj.position = pg.Vector2(100, 100)
env_obj.obj_shadow = '32x16'

# Add them to the game object group
game.game_object_group.add(player, env_obj, enemy)

# Rescale GameObjects to have a SCALE of 3 (this makes them more visible)
tde.GameObject.set_scale(3, game)

# GameObj automatically generates a four frame "flashing animation."
# In order have our EnvObj not flash, we will make it use only the first frame.
env_obj.animations['idle'] = [env_obj.animations['idle'][0]]

# You can add subpixel rendering by uncommenting the below line of code.
# tde.GameObject.SUBPIXEL = True

# Run the game
game.run()