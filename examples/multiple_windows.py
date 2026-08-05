import topdownengine as tde
from topdownengine.mobile_object.controller import KeyboardInputController, MovementAIController
import pygame as pg
from topdownengine.ui import Button, UIContainer, Text

# Define an instance of the Game class
game = tde.Game(
    screen_width=900, 
    screen_height=650, 
    window_title="pygame-topdownengine Multiple Windows Example",
    target_scale=3 # Add scale of three to make it more visible
)
game.bg_color = (40, 229, 30)

# Define main menu using a BaseScene instance + set the active scene to the main menu
game.scenes["menu"] = tde.BaseScene(game)
game.active_scene_key = "menu"

# Create the play button + header
font = tde.Font("Arial")
header = Text((450, 200), font, 50, "pygame-topdownengine", (255, 255, 255))

play_btn = Button((450, 350), on_click=lambda: setattr(game, "active_scene_key", "gameplay"))
play_btn.image = pg.Surface((150, 50))
play_btn.image.fill((50, 100, 100))
font.draw_text("PLAY", 75, 25, 40, play_btn.image, (255, 255, 255))

# Add the header + play button to the main menu
container = UIContainer()
container.add_ui_element(header)
container.add_ui_element(play_btn)
game.scenes["menu"].ui_containers.append(container)

# Define a MobileObject to be the Player + Enable Camera Tracking
player = tde.MobileObject(
    controller=KeyboardInputController(), 
    animation_paths={
        "idle": tde.ASSETS_DIR / "example-player" / "idle.png",
        "walk": tde.ASSETS_DIR / "example-player" / "walk.png"
    }, frame_size=(16, 16), directional_anims=True
)
# game.camera = tde.SmoothTrackerCamera(game) # Uncomment to enable Smooth Tracking
game.camera.focus_game_object = player

# Define a MobileObject to follow the Player
enemy = tde.MobileObject(
    controller=MovementAIController(target_mobile_object=player), 
    animation_paths=player.animation_paths, # Use same animations as the Player
    frame_size=(16, 16), directional_anims=True
)

# Define an EnvObject
env_object = tde.EnvObject(
    animation_paths={
        "idle": tde.ASSETS_DIR / "example-cliff.png"
    },
    frame_size=(32, 32), colliders=[pg.Rect(0, 0, 32, 32)]
)
env_object.position = pg.Vector2(100, 100)
env_object.obj_shadow = "32x16"

# Add them to the game object group
game.game_object_group.add(player, env_object, enemy)

# You can add subpixel rendering by uncommenting the below line of code.
# tde.GameObject.SUBPIXEL = True

# Lighting
game.scenes["gameplay"].global_alpha = 150
player.light_radius = 24
enemy.light_radius = 24

# Debug Menu
game.scenes["debug_menu"] = tde.BaseScene(game)
debug_container = UIContainer()
debug_toggle = Button(
    (150, 50),
    on_click=lambda: setattr(game, "debug", not game.debug)
)
debug_toggle.image = pg.Surface((250, 50))
debug_toggle.image.fill((150, 50, 50))
font.draw_text("TOGGLE DEBUG RENDERING", 125, 25, 20, debug_toggle.image, (255, 255, 255))

spawn_btn = Button(
    (150, 125),
    on_click=lambda: game.game_object_group.add(
        tde.MobileObject(
            controller=MovementAIController(target_mobile_object=player), 
            animation_paths=player.animation_paths, # Use same animations as the Player
            frame_size=(16, 16), directional_anims=True
        )
    )
)
spawn_btn.image = pg.Surface((250, 50))
spawn_btn.image.fill((150, 50, 50))
font.draw_text("SPAWN ENEMY", 125, 25, 20, spawn_btn.image, (255, 255, 255))

debug_container.add_ui_element(debug_toggle)
debug_container.add_ui_element(spawn_btn)
game.scenes["debug_menu"].ui_containers.append(debug_container)

window = pg.Window()
window.size = (300, 400)
window.title = "Debug Menu"

# Register the new window into the extra_windows dictionary and make it use the "debug_menu" scene.
game.extra_windows[window] = "debug_menu"

# Run the game
game.run()