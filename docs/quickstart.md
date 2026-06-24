---
layout: page
title: "Quickstart"
---
# Quickstart

## Introduction
In this quickstart, we will be guiding you towards creating a Player character you can move with WASD on your keyboard, a secondary character that will attempt to follow the Player, and a solid object the Player can collide with and jump over.

## Importing Dependencies
Let's get the ball rolling! Before we can do anything however, we will need to import the engine and pygame-ce.
```
# Import the main engine
import topdownengine as tde

# The first import allows for keyboard-based movement and the second one allows for AI-based movement.
from topdownengine.mobile_object.controller import KeyboardInputController, MovementAIController

# We will need this for pre-made animations the package comes with.
from topdownengine.asset_paths import ASSETS_DIR

# pygame-ce provides us with some really helpful utilities.
import pygame as pg
```

## The Game Class
Great! Now that we have imported everything, let's define the first thing you will define in every project you make. The Game class mainly functions as a wrapper for updates and rendering, but it is also used by individual GameObjects for a variety of things.
```
# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example",
    target_scale=3 # Add scale of three to make it more visible
)
game.bg_color = (40, 229, 30) # Give it a background color
```

## The Player
Now that we have a Game instance, the next thing we will define is the Player. This code gives the player keyboard movement and animations (using the package's premade animations). It uses a MobileObject, which is a subclass of the GameObject class with extra movement features. For reference, GameObject is the base class for all in-world objects in the engine.
```
# Define a MobileObject to be the Player + Enable Camera Tracking
player = tde.MobileObject(
    controller=KeyboardInputController(), 
    animation_paths={
        "idle": ASSETS_DIR / "example-player" / "idle.png",
        "walk": ASSETS_DIR / "example-player" / "walk.png"
    }, frame_size=(16, 16), directional_anims=True
)
game.camera.focus_game_object = player
```

## The Enemy
Now let's make the character that follows you. For the purposes of this tutorial, let's call it the "enemy". This code makes the enemy follow the player and uses the same animations as the Player itself.
```
# Define a MobileObject to follow the Player
enemy = tde.MobileObject(
    controller=MovementAIController(target_mobile_obj=player), 
    animation_paths=player.animation_paths, # Use same animations as the Player
    frame_size=(16, 16), directional_anims=True
)
```

## EnvObject
Now let's define a box the player can collide with and jump over. Essentially, this code will make the box 32x32 in world space, give it a shadow, and set its position away from (0, 0), which is the default position for all GameObjects. The EnvObject class is a subclass of the GameObject class, similar to MobileObject.
```
env_object = tde.EnvObject(
    animation_paths={
        "idle": ASSETS_DIR / "example-cliff.png"
    },
    frame_size=(32, 32), colliders=[pg.Rect(0, 0, 32, 32)]
)
env_object.position = pg.Vector2(100, 100)
env_object.obj_shadow = "32x16"
```

## Adding Them to the Game
Now, we need to add these three to the actual game itself. In order to do that, we add each one to the Game instance's `game_object_group`.
```
# Add them to the game object group
game.game_object_group.add(player, env_object, enemy)
```

## Subpixel vs Pixel-Perfect Rendering
pygame-topdownengine offers both pixel-perfect rendering and subpixel rendering out of the box. By default, pixel-perfect rendering is used. However, if you want subpixel rendering to make it more smooth, you can do that with this code:
```
tde.GameObject.SUBPIXEL = True
```

## Execution
You made it! If you got to this point in this tutorial, you're almost there. Before everything's well and done, we need to actually run the game. To do that, we call the `run` method on the Game instance as shown below:

```
# Run the game
game.run()
```

If everything went right, you should have a character you can control with WASD (with Space for jump), another character that follows you, and a red box you can jump over and collide with! If all's not well, check out the example code on [GitHub](https://github.com/shaurya-sharma-dev/pygame-topdownengine/blob/main/examples/basic_usage.py) to see what went wrong.