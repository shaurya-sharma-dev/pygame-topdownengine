# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pytest
import pygame as pg

@pytest.mark.parametrize("position", [
    pg.Vector2(5, 8),
    pg.Vector2(4, 7),
    pg.Vector2(5, 9),
    pg.Vector2(8, 5),
    pg.Vector2(5, 3),
    pg.Vector2(7, 9),
    pg.Vector2(5, 7),
    pg.Vector2(4, 6),
    pg.Vector2(3, 2),
])
def test_base_camera_instantly_snaps_to_position_if_focus_game_object_is_set(game: tde.Game, position: pg.Vector2):
    game_object = tde.GameObject()
    game.game_object_group.add(game_object)
    game.camera.focus_game_object = game_object

    game_object.position = position
    game.update(1000 / game.fps)

    assert game_object.position - pg.Vector2(
        game.screen.width / tde.GameObject.SCALE / 2, 
        game.screen.height / tde.GameObject.SCALE / 2
    ) == game.camera.real_position