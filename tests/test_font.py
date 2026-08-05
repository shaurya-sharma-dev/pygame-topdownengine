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

# TODO: Add more paramatrized values.
@pytest.mark.parametrize("text,target_rect,expected_size", [
    ["test", pg.Rect(0, 0, 100, 50), 50],
    ["test", pg.Rect(0, 0, 100, 1), 2]
])
def test_get_max_size_for_text_in_rect_method(game: tde.Game, text: str, target_rect: pg.Rect, expected_size: int):
    font = tde.Font("Arial")
    assert font.get_max_size_for_text_in_rect(text, target_rect) == expected_size