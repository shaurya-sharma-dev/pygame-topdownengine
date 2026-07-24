# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pytest
import pygame as pg
from conftest import FAKED_KEYS
from topdownengine.mobile_object.controller import KeyboardInputController, StaticController, BaseController

# Jump Tests
def test_does_jump_if_jump_called_while_grounded(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.elevation = mobile_object.z = 0
    mobile_object.jump()
    assert mobile_object.z_vel == mobile_object.jump_vel

def test_does_not_jump_if_jump_called_while_airborne(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.elevation = 0
    mobile_object.z = 10
    mobile_object.jump()
    assert mobile_object.z_vel != mobile_object.jump_vel

# 2D Movement Tests
MOVEMENT_TEST_ARGS = [
    pg.Vector2(1, 0),  # Right
    pg.Vector2(0, 1),  # Down
    pg.Vector2(-1, 0), # Left
    pg.Vector2(0, -1), # Up
    pg.Vector2(1, 1),  # Down-Right
    pg.Vector2(1, -1), # Up-Right
    pg.Vector2(-1, 1), # Down-Left
    pg.Vector2(-1, -1) # Up-Left
]
@pytest.mark.parametrize("dir", MOVEMENT_TEST_ARGS)
def test_velocity_matches_direction_if_stationary_with_keyboard_input_controller_active(game: tde.Game, mobile_object: tde.MobileObject, dir: pg.Vector2):
    mobile_object.controller = KeyboardInputController()
    game.game_object_group.add(mobile_object)

    def step(key, condition):
        FAKED_KEYS.clear()
        FAKED_KEYS.add(key)
        
        # For some reason, this line fixes an error where pytest says mobile_object is undefined during the eval call.
        mobile_object

        game.update(1000 / game.fps)
        assert eval(condition)

    if dir.x == 1:
        step(pg.K_d, "mobile_object.velocity.x > 0")

    elif dir.x == -1: 
        step(pg.K_a, "mobile_object.velocity.x < 0") 

    if dir.y == 1:
        step(pg.K_s, "mobile_object.velocity.y > 0")

    elif dir.y == -1: 
        step(pg.K_w, "mobile_object.velocity.y < 0")

def test_velocity_does_not_affect_mobile_object_position_if_using_static_controller(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.controller = StaticController()
    game.game_object_group.add(mobile_object)

    mobile_object.velocity = pg.Vector2(999, 999)
    game.update(1000 / game.fps)

    assert mobile_object.velocity == pg.Vector2()
    assert mobile_object.position == pg.Vector2()

def test_position_and_velocity_remain_constant_if_update_called_with_base_controller(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.controller = BaseController()
    game.game_object_group.add(mobile_object)

    game.update(1000 / game.fps)

    assert mobile_object.position == pg.Vector2()
    assert mobile_object.velocity == pg.Vector2()