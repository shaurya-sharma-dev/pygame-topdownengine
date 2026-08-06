# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pytest
import pygame as pg

# GameObjectGroup Tests
# We add the game fixture to initialize the display.

@pytest.mark.usefixtures("game")
class TestGameObjectGroup:
    def test_contains_game_object_if_game_object_was_added_by_group(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        group.add(game_object)

        assert group in game_object.groups

    def test_contains_game_object_if_group_was_added_by_game_object(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)

        assert game_object in group.game_objects

    def test_does_not_contain_game_object_if_removed_by_game_object(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)
        game_object.remove_from(group)

        assert game_object not in group.game_objects

    def test_does_not_contain_game_object_if_removed_by_group(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        game_object.add_to(group)
        group.remove(game_object)

        assert game_object not in group.game_objects

    def test_game_object_is_added_and_removed_if_modifying_game_object_group_game_objects_set_directly(self):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()

        group.game_objects = {game_object,}

        assert game_object in group.game_objects
        assert group in game_object.groups

        group.game_objects = set()

        assert game_object not in group.game_objects
        assert group not in game_object.groups

    def test_game_objects_in_a_group_are_updated_if_the_group_update_method_is_called(self, game: tde.Game):
        group = tde.GameObjectGroup()
        game_object = tde.GameObject()
        game_object.velocity = pg.Vector2(game_object.VELOCITY_DEADZONE + 1, game_object.VELOCITY_DEADZONE + 1)

        group.add(game_object)

        group.update(1000 / game.fps, game)
        assert game_object.position != pg.Vector2()

# Velocity Deadzone Tests
def test_clears_velocity_if_in_velocity_deadzone_range(game: tde.Game):
    game_object = tde.GameObject()
    game.game_object_group.add(game_object)

    game_object.velocity = pg.Vector2(game_object.VELOCITY_DEADZONE, 0)
    game_object.update(1000 / game.fps, game)

    assert game_object.velocity == pg.Vector2()

def test_does_not_clear_velocity_if_not_in_velocity_deadzone_range(game: tde.Game):
    game_object = tde.GameObject()
    game.game_object_group.add(game_object)

    game_object.velocity = pg.Vector2(game_object.VELOCITY_DEADZONE + 0.1, 0)
    game_object.update(1000 / game.fps, game)

    assert game_object.velocity != pg.Vector2()

# Pixel Perfect vs. Subpixel Rendering
# Add game fixture to initialize display.
def test_game_object_rect_attribute_is_rect_if_subpixel_rendering_is_disabled(game: tde.Game):
    # Subpixel rendering is disabled by default.

    game_object = tde.GameObject()
    assert type(game_object.rect) == pg.Rect

def test_game_object_rect_attribute_is_frect_if_subpixel_rendering_is_enabled(game: tde.Game):
    tde.GameObject.SUBPIXEL = True
    game_object = tde.GameObject()
    assert type(game_object.rect) == pg.FRect

# Scaling
@pytest.mark.parametrize("scale_by", range(2, 10))
def test_game_object_frame_size_is_modified_correctly_if_set_scale_is_called_with_game_object_in_game_object_group(game: tde.Game, scale_by: int):
    game_object = tde.GameObject()
    start_frame_size = pg.Vector2(16, 16) # Default frame_size is 16x16 pixels.
    game.game_object_group.add(game_object)
    tde.GameObject.set_scale(scale_by, game)

    assert start_frame_size * scale_by == pg.Vector2(game_object.animations["idle"][0].size)

# Collisions
def test_handle_collision_method_raises_value_error_if_both_axes_are_non_zero(game: tde.Game):
    game_object = tde.GameObject()
    with pytest.raises(ValueError, match="Both axes cannot be moved in one step. Move them in separate method calls."):
        game_object.handle_collision(pg.Vector2(1, 1), game)

# Elevation
def test_game_object_elevated_if_handle_elevation_called_while_intersecting(game: tde.Game):
    game_object = tde.GameObject()
    env_object = tde.EnvObject(
        animation_paths={
            "idle": tde.ASSETS_DIR / "example-cliff.png"
        },
        frame_size=(32, 32), colliders=[pg.Rect(0, 0, 32, 32)]
    )

    game.game_object_group.add(game_object, env_object)
    game_object.handle_elevation(game)
    assert game_object.elevation == env_object.height