# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pygame as pg
import pytest

def test_value_error_raised_if_game_init_given_invalid_extra_feature():
    item = "INVALID EXTRA FEATURE"
    expected_error = (
        f"'{item}' is not a valid extra feature and does nothing. "
        f"Please choose from: {list(tde.Game.VALID_EXTRA_FEATURES)}"
    )

    with pytest.raises(ValueError, check=lambda e: str(e) == expected_error):
        tde.Game(1, 1, extra_features=[item])

def test_active_scene_property_returns_correct_scene_if_active_scene_key_attribute_is_modified(game: tde.Game):
    game.scenes["another scene"] = tde.BaseScene(game)
    assert game.active_scene == game.scenes[game.active_scene_key]

    game.active_scene_key = "another scene"
    assert game.active_scene == game.scenes[game.active_scene_key]