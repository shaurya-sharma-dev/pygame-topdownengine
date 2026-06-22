# pygame-topdownengine
[![License: MIT](https://img.shields.io/pypi/l/pygame-topdownengine)](https://github.com/shaurya-sharma-dev/pygame-topdownengine/blob/main/LICENSE)
[![PyPI Version](https://img.shields.io/pypi/v/pygame-topdownengine)](https://pypi.org/project/pygame-topdownengine/)
[![Python Versions](https://img.shields.io/pypi/pyversions/pygame-topdownengine)](https://pypi.org/project/pygame-topdownengine/)
[![Types: Typed](https://img.shields.io/pypi/types/pygame-topdownengine)](https://pypi.org/project/pygame-topdownengine/)

pygame-topdownengine is a 2.5D engine for top-down games. It is designed to be highly modular, with most core systems being located in the easily extendible GameObject class. It is built on top of the pygame-ce package, which you can find here: https://github.com/pygame-community/pygame-ce/tree/main.

## Features
- `GameObject` class that contains all of the core systems.
- `MobileObject` class that allows for modular movement behavior.
- `EnvObject` class for environmental decorations or objects.
- Built in `VisualUtils` class that allows for the easy manipulation of Surfaces.
- Option to use either pixel-perfect or subpixel rendering.
- Dynamic scale-setting for all `GameObject` instances.
- Robust 3D collision detection.
- Toggleable `Game.debug` attribute to render hitboxes during development.

## Quickstart
This code makes a Player character, a secondary character that will attempt to follow the Player character, and a solid object the Player can collide with and jump over.
```
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
```

## Installation
In order to install pygame-topdownengine, make sure Python and pip are both installed and in PATH. Then, run this command into your terminal:<br>
`pip install pygame-topdownengine`

## License
This library is distributed under the MIT license, which can be found in the root of this repository under the `LICENSE` file.

The source files located in the `examples` subfolder are licensed under the Creative Commons Zero 1.0 Universal license, which can be found inside of `examples/LICENSE`.