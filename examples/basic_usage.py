import topdownengine as tde
from topdownengine.mob_controller import KeyboardInputController

# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a mob
game_object = tde.Mob(controller=KeyboardInputController())

# Add it to the game object group
game.game_object_group.add(game_object)

# Rescale GameObjects to have a SCALE of 2 (this makes them more visible)
tde.GameObject.set_scale(2, game)

# Run the game
game.run()