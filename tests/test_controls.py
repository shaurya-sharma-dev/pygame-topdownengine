# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
from topdownengine.controls import KeyboardInputManager, NoKeysPressed
import pygame as pg

class TestKeyboardInputManager:
    def test_deserializing_creates_same_keybinds_dict_if_using_serialized_version_of_original_keybinds_dict(self):
        manager = KeyboardInputManager()
        manager.keybinds["Custom Keybind"] = pg.K_AC_BACK
        serialized_manager_keybinds = manager.serialize()

        new_manager = KeyboardInputManager()
        new_manager.deserialize(serialized_manager_keybinds)

        assert manager.keybinds == new_manager.keybinds

def test_getting_index_value_is_equal_to_false_if_using_no_keys_pressed_instance():
    assert not NoKeysPressed()[0]