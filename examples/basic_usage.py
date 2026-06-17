import topdownengine as tdg

# Define an instance of the Game class
game = tdg.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Basic Usage Example"
)

# Define a game object
game_object = tdg.GameObject()

# Add it to the game object group
game.game_object_group.add(game_object)

# Run the game
game.run()