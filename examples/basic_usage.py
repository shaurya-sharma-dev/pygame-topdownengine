import topdownengine as tde
from topdownengine.mob_controller import KeyboardInputController
from topdownengine.asset_paths import ASSETS_DIR

# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a mob
game_object = tde.Mob(
    controller=KeyboardInputController(), 
    animation_paths={
        'idle': ASSETS_DIR / 'example-player' / 'idle.png',
        'walk': ASSETS_DIR / 'example-player' / 'walk.png'
    },
    frame_size=(16, 16),
    directional_anims=True
)

# Add it to the game object group
game.game_object_group.add(game_object)

# Rescale GameObjects to have a SCALE of 3 (this makes them more visible)
tde.GameObject.set_scale(3, game)

# Run the game
game.run()