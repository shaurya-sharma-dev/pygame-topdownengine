---
layout: page
title: "Game"
---
# Game

Acts as the central core of the game and manages the core loop and gamestate.
    
## Attributes

- `screen` (pygame.Surface): The primary display Surface.
- `is_running` (bool): Boolean flag to control execution.
- `clock` (pygame.time.Clock): Controls framerate and handles deltatime.
- `fps` (int): Integer that controls how much FPS the Game should have
- `game_object_group` (pygame.sprite.Group): Stores all GameObjects.
- `game_speed_percentage` (float): The speed percentage for execution, ranging from `0` to `1`.
- `debug` (bool): If `True`, debug rendering will be enabled.
- `target_ratio` (float): Target aspect ratio for resizing.
- `target_scale` (int): The target scale for the original window size.
- `og_width` (int): Original window width.
- `extra_features` (list[str]): List of extra features to add at runtime. You MUST set it during instantiation.