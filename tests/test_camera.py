# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pytest
import pygame as pg
import math

POSITIONS = [
    pg.Vector2(5, 8),
    pg.Vector2(4, 7),
    pg.Vector2(5, 9),
    pg.Vector2(8, 5),
    pg.Vector2(5, 3),
    pg.Vector2(7, 9),
    pg.Vector2(5, 7),
    pg.Vector2(4, 6),
    pg.Vector2(3, 2),
]

@pytest.mark.parametrize("position", POSITIONS)
def test_base_camera_instantly_snaps_to_position_if_focus_game_object_is_set(game: tde.Game, position: pg.Vector2):
    game_object = tde.GameObject()
    game.game_object_group.add(game_object)
    game.camera.focus_game_object = game_object

    game_object.position = position
    game.camera.update(1000 / game.fps)

    assert game_object.position - pg.Vector2(
        game.screen.width / tde.GameObject.SCALE / 2, 
        game.screen.height / tde.GameObject.SCALE / 2
    ) == game.camera.real_position

@pytest.mark.parametrize("position", POSITIONS)
@pytest.mark.parametrize("intensity", range(1, 4)) # Use intensities of 1, 2, and 3 because the lowest distance from (0, 0) is ~3.6.
def test_distance_of_position_from_real_position_within_intensity_times_sqrt_2_if_screenshake_set_on_base_camera(game: tde.Game, position: pg.Vector2, intensity: int):
    game.camera.real_position = position
    game.camera.screenshake = {"duration": 99, "intensity": intensity}
    game.camera.update(1000 / game.fps)

    # Test that the distance between screenshake position and real position is within
    # intensity multiplied by the square root of 2.
    assert game.camera.real_position.distance_to(game.camera.position) <= intensity * math.sqrt(2)

@pytest.mark.parametrize("position", POSITIONS)
def test_focus_game_object_is_tracked_smoothly_if_smooth_tracker_camera_is_active(game: tde.Game, position: pg.Vector2):
    game_object = tde.GameObject()
    game_object.position = position
    game.game_object_group.add(game_object)

    game.camera = tde.SmoothTrackerCamera(game)
    game.camera.focus_game_object = game_object

    dt = 1000 / game.fps

    expected_target_position = pg.Vector2(game_object.position) - pg.Vector2(
        game.screen.width / game_object.SCALE / 2, 
        game.screen.height / game_object.SCALE / 2
    )

    expected_real_position = ((expected_target_position - game.camera.real_position) * (dt / 1000) * 5)

    game.camera.update(dt)

    assert game.camera.real_position.x == pytest.approx(expected_real_position.x)
    assert game.camera.real_position.y == pytest.approx(expected_real_position.y)