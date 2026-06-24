# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import os

# Set dummy drivers before importing pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import topdownengine as tde
import pytest
import pygame as pg
from conftest import FAKED_KEYS

# Jump Tests
def test_can_jump_while_grounded(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.elevation = mobile_object.z = 0
    mobile_object.jump()
    assert mobile_object.z_vel == mobile_object.jump_vel

def test_cannot_jump_while_airborne(game: tde.Game, mobile_object: tde.MobileObject):
    mobile_object.elevation = 0
    mobile_object.z = 10
    mobile_object.jump()
    assert mobile_object.z_vel != mobile_object.jump_vel

# 2D Movement Tests
MOVEMENT_TEST_ARGS = [
    pg.Vector2(1, 0), # Right
    pg.Vector2(0, 1), # Down
    pg.Vector2(-1, 0), # Left
    pg.Vector2(0, -1), # Up
    pg.Vector2(1, 1), # Down-Right
    pg.Vector2(1, -1), # Up-Right
    pg.Vector2(-1, 1), # Down-Left
    pg.Vector2(-1, -1) # Up-Left
]
@pytest.mark.parametrize("dir", MOVEMENT_TEST_ARGS)
def test_movement(game: tde.Game, mobile_object: tde.MobileObject, dir: pg.Vector2):
    def step(key, condition):
        FAKED_KEYS.clear()
        FAKED_KEYS.add(key)
        game.handle_events()
        mobile_object.update(60, game)
        assert eval(condition)

    if dir.x == 1:
        step(pg.K_d, "mobile_object.velocity.x > 0")

    elif dir.x == -1: 
        step(pg.K_a, "mobile_object.velocity.x < 0") 

    if dir.y == 1:
        step(pg.K_s, "mobile_object.velocity.y > 0")

    elif dir.y == -1: 
        step(pg.K_w, "mobile_object.velocity.y < 0")