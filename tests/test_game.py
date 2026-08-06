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

def test_core_methods_are_called_in_correct_order_if_run_method_called(game: tde.Game, monkeypatch):
    execution_order = []

    # Mock methods
    def mock_handle_events(self):
        execution_order.append("handle_events")

    def mock_update(self, dt: float):
        execution_order.append("update")
        self.is_running = False # Break in first frame

    def mock_render(self):
        execution_order.append("render")

    def mock_quit(self):
        execution_order.append("quit")

    monkeypatch.setattr(tde.Game, "handle_events", mock_handle_events)
    monkeypatch.setattr(tde.Game, "update", mock_update)
    monkeypatch.setattr(tde.Game, "render", mock_render)
    monkeypatch.setattr(tde.Game, "quit", mock_quit)
    
    game.is_running = True
    game.run()

    assert execution_order == ["handle_events", "update", "render", "quit"]