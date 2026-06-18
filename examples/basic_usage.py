import topdownengine as tdg
from topdownengine.mob_controller import KeyboardInputController

# Define an instance of the Game class
game = tdg.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a mob
game_object = tdg.Mob(controller=KeyboardInputController())

# Add it to the game object group
game.game_object_group.add(game_object)

# Run the game
game.run()