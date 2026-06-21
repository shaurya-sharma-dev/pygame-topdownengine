# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
from pygame._sdl2.controller import Controller

class KeyboardInputManager:
    """Acts as a keyboard and mouse input reciever.
    
    Attributes:
        keybinds (dict[str,int|str]): Stores all keybind data.
        non_hold_inputs (list[str]): List of which inputs can't be held.
        keys (pg.key.ScancodeWrapper): Keys currently pressed.
        just_pressed_keys (pg.key.ScancodeWrapper): Keys pressed in the current frame.
    """

    def __init__(self) -> None:
        self.keybinds = {
            'Move Right': pg.K_d,
            'Move Left': pg.K_a,
            'Move Up': pg.K_w,
            'Move Down': pg.K_s,
            'Jump': pg.K_SPACE
        }
        self.non_hold_inputs = []

    def serialize(self) -> dict:
        return {
            k: pg.key.name(v) if type(v) == int else v
            for k, v in self.keybinds.items()
        }
    
    def deserialize(self, data: dict) -> None:
        for k, v in data.items():
            try:
                self.keybinds[k] = pg.key.key_code(v)
            except ValueError:
                self.keybinds[k] = v
    
    def get_input(self) -> list[str]:
        "Returns all inputs to execute logic for. MUST be called after pg.event.get()."
        self.keys = pg.key.get_pressed()
        self.just_pressed_keys = pg.key.get_just_pressed()
        inputs = []

        for keybind in self.keybinds:
            if self.keybinds[keybind] == 'Button 1':
                if pg.mouse.get_just_pressed()[0]: 
                    inputs.append(keybind) 
            elif self.keybinds[keybind] == 'Button 3':
                if pg.mouse.get_just_pressed()[2]: 
                    inputs.append(keybind) 
            else:
                if self.keys[self.keybinds[keybind]]: 
                    if keybind in self.non_hold_inputs:
                        if self.just_pressed_keys[self.keybinds[keybind]]:
                            inputs.append(keybind)
                    else:
                        inputs.append(keybind) 

        return inputs

# TODO: Add controller support
# class ControllerInputManager:
#     def __init__(self):
#         self.controller = Controller(0)

#         self.keybinds = {
#             # 'Interact': pg.K_e,
#             # 'Inventory': pg.K_i,
#             'Use Item': pg.CONTROLLER_BUTTON_RIGHTSHOULDER,
#             'Use Item Special': 5,
#             # 'Use Ability 1': pg.K_v,
#             # 'Use Ability 2': pg.K_b,
#         }
#         self.non_hold_inputs = ['Interact', 'Inventory']

#     def get_input(self) -> list[str]:
#         inputs = []

#         for keybind in self.keybinds:
#             print(self.controller.get_button(self.keybinds[keybind]))
#             if self.controller.get_button(self.keybinds[keybind]): 
#                 if keybind in self.non_hold_inputs and False:
#                     if self.just_pressed_keys[self.keybinds[keybind]]:
#                         inputs.append(keybind)
#                 else:
#                     inputs.append(keybind) 
#                     print('hello')
#         return inputs

class NoKeysPressed:
    "Emulates a pygame ScancodeWrapper where no keys are pressed."
    def __getitem__(self, key: int) -> bool: 
        return False

class MoreKeysPressed:
    """Emulates a pygame ScancodeWrapper where given keys are always pressed.

    Args:
        wrapper: The wrapper to add keys to.
        pressed_keys: The keys to add to the wrapper.
        
    Attributes:
        wrapper: The base wrapper that keys were added to.
        pressed_keys: The keys added to the wrapper.
    """

    def __init__(self, wrapper: pg.key.ScancodeWrapper, pressed_keys: set[int]) -> None: 
        self.wrapper = wrapper
        self.pressed_keys = pressed_keys

    def __getitem__(self, key: int) -> bool:
        return self.wrapper[key] or key in self.pressed_keys