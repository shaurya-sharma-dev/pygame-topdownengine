# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
import pygame as pg
import pytest

def test_draw_text_method_raises_value_error_if_given_invalid_align_value(game: tde.Game):
    font = tde.Font("Arial")
    surf = pg.Surface((1,1))
    with pytest.raises(ValueError):
        font.draw_text("test", 0, 0, 1, surf, "black", "invalid alignment")