# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
import pytest
import topdownengine as tde
from topdownengine.mobile_obj.controller import KeyboardInputController
from topdownengine.asset_paths import ASSETS_DIR
from topdownengine.controls import MoreKeysPressed

# Fixtures
@pytest.fixture
def game():
    game = tde.Game(1, 1)
    print('Initializing game instance.')
    yield game
    pg.quit()

@pytest.fixture
def mobile_obj():
    return tde.MobileObj(
        controller=KeyboardInputController(), 
        animation_paths={
            'idle': ASSETS_DIR / 'example-player' / 'idle.png',
            'walk': ASSETS_DIR / 'example-player' / 'walk.png'
        },
        frame_size=(16, 16),
        directional_anims=True
    )

# This code "monkey patches" pygame-ce to replace get_pressed with a custom
# function that allows us to add/remove fake keys to the stream by 
# adding/removing them from the FAKED_KEYS set.
FAKED_KEYS = set()
original_get_pressed = pg.key.get_pressed

def fake_get_pressed():
    return MoreKeysPressed(original_get_pressed(), FAKED_KEYS)

pg.key.get_pressed = fake_get_pressed