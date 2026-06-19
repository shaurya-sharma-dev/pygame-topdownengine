import topdownengine as tde
from topdownengine.mobile_obj.controller import KeyboardInputController
from topdownengine.asset_paths import ASSETS_DIR
from topdownengine.math import scale_rect
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
env_obj = tde.EnvObject(frame_size=(32, 32), colliders=[pg.Rect(0, 0, 32, 32)])
env_obj.position = pg.Vector2(100, 100)
env_obj.obj_shadow = '32x16'

# Add them both to the game object group
game.game_object_group.add(mobile_obj)
game.game_object_group.add(env_obj)

# Rescale GameObjects to have a SCALE of 3 (this makes them more visible)
tde.GameObject.set_scale(3, game)

# GameObj automatically generates a four frame "flashing animation."
# In order to disable it, this line of code makes it use only the first frame,
# which is solid red.
env_obj.animations = {'idle': [env_obj.animations['idle'][0]]} 

# You can add subpixel rendering by uncommenting the below line of code
# tde.GameObject.SUBPIXEL = True

# Debug Rendering
# original_draw = game.render
# def new_render():
#     original_draw()
#     pg.draw.rect(
#         game.screen, 
#         (0, 0, 255), 
#         scale_rect(mobile_obj.hitboxes[0], mobile_obj.SCALE),
#         1
#     )
#     pg.draw.rect(
#         game.screen, 
#         (0, 0, 255), 
#         scale_rect(env_obj.hitboxes[0], env_obj.SCALE),
#         1
#     )
#     pg.display.flip()

# game.render = new_render

# Run the game
game.run()