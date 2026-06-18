# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import os

# Set dummy drivers before importing pygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import topdownengine as tde
from topdownengine.mob_controller import BaseMobController
from topdownengine.asset_paths import ASSETS_DIR
import pytest
import pygame as pg

pg.init()
pg.display.set_mode((1,1))

@pytest.fixture
def mob():
    return tde.Mob(
        controller=BaseMobController(), 
        animation_paths={
            'idle': ASSETS_DIR / 'example-player' / 'idle.png',
            'walk': ASSETS_DIR / 'example-player' / 'walk.png'
        },
        frame_size=(16, 16),
        directional_anims=True
    )

# Jump Tests
def test_can_jump_while_grounded(mob):
    mob.elevation = mob.z = 0
    mob.jump()
    assert mob.z_vel == mob.jump_vel

def test_cannot_jump_while_airborne(mob):
    mob.elevation = 0
    mob.z = 10
    mob.jump()
    assert mob.z_vel != mob.jump_vel

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
def test_movement(mob, dir):
    pass