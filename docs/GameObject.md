---
layout: page
title: "GameObject"
---
# GameObject

This class is the base class for all in-world objects in the engine.
    
## Attributes
- `SCALE` (int): How much to scale all GameObjects by (do not set directly, use `GameObject.set_scale`)
- `SHADOWS` (dict[str, pg.Surface]): Dictionary of shadow images, loaded automatically once you instantiate a `GameObject`. **DO NOT MODIFY MANUALLY.**
- `SUBPIXEL` (bool): Whether to use subpixel rendering or not. You must set it at the class level.
- `VELOCITY_DEADZONE` (float): Minimum magnitude for `velocity` before it gets set to `(0, 0)`.
- `CAUSES_COLLISONS` (bool): Can this `GameObject` cause other `GameObjects` to collide with it?
- `position` (pg.Vector2): Current world-space position of the `GameObject`.
- `velocity` (pg.Vector2): Current world-space velocity of the `GameObject`.
- `elevation` (int): Current world-space elevation of the `GameObject`.
- `z` (float): Current world-space z-position of the `GameObject`.
- `z_vel` (float): Current world-space z-velocity of the `GameObject`.
- `gravity` (float): World-space gravity of the `GameObject`.
- `height` (float): World-space height of the `GameObject`.
- `frame` (float): Current animation frame.
- `anim_speed` (float): Animation speed.
- `current_animation` (str): Current animation.
- `obj_shadow` (str|None): Shadow size being used (or None for no shadow).
- `colliders` (list[pg.Rect|pg.FRect]): List of hitboxes relative to the `GameObject`.
- `hitboxes` (list[pg.Rect|pg.FRect]): List of world-space hitboxes in the current frame.
- `current_frame` (pg.Surface): Current animation frame surface.
- `image` (pg.Surface): Image for drawing (includes `current_frame` and the shadow).
- `rect` (pg.Rect|pg.FRect): Rect object for drawing.
- `draw_index` (tuple[float]): Sorting index for drawing.