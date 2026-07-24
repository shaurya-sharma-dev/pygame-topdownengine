# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from topdownengine import math as tde_math
import pygame as pg
import pytest

@pytest.mark.parametrize("start, end", [
    [5, 8],    # P -> P
    [1, -7],   # P -> N
    [5, 0],    # P -> 0
    [-8, 5],   # N -> P
    [-5, -10], # N -> N
    [-7, 0],   # N -> 0
    [0, 7],    # 0 -> P
    [0, -6],   # 0 -> N
    [0, 0],    # 0 -> 0
])
class TestLerp:
    def test_result_equals_start_if_t_equals_0(self, start, end):
        assert tde_math.lerp(start, end, 0) == start

    def test_result_equals_end_if_t_equals_1(self, start, end):
        assert tde_math.lerp(start, end, 1) == end

    def test_raises_type_error_for_mismatched_types(self, start, end):
        # Rather than use the start and end parameters for their purpose in the other tests,
        # we use it in this test to ensure it still raises the exception regardless of the value,
        # as long as types are misaligned.
        with pytest.raises(TypeError):
            tde_math.lerp(pg.Vector2(start, end), start, 1)

class TestScaleRect:
    @pytest.fixture(params=range(1, 11), scope="class")
    @classmethod
    def scalar(cls, request):
        return request.param

    def test_scaled_rect_area_is_equal_to_original_area_times_scalar_squared_if_scalar_is_positive(self, scalar):
        og_rect = pg.Rect(0, 0, 3, 4)
        scaled_rect = tde_math.scale_rect(og_rect, scalar)

        assert og_rect.width * og_rect.height * (scalar ** 2) == scaled_rect.width * scaled_rect.height

    def test_scaled_rect_position_is_equal_to_original_position_times_scalar_if_scalar_is_positive(self, scalar):
        og_rect = pg.Rect(1, 1, 3, 4)
        scaled_rect = tde_math.scale_rect(og_rect, scalar)

        assert pg.Vector2(og_rect.topleft) * scalar == pg.Vector2(scaled_rect.topleft)

    def test_value_error_is_raised_if_scalar_is_zero(self):
        with pytest.raises(ValueError, match="Scalar must be greater than 0."):
            og_rect = pg.Rect(1, 1, 3, 4)
            tde_math.scale_rect(og_rect, 0)

    def test_value_error_is_raised_if_scalar_is_negative(self, scalar):
        with pytest.raises(ValueError, match="Scalar must be greater than 0."):
            og_rect = pg.Rect(1, 1, 3, 4)
            tde_math.scale_rect(og_rect, -scalar)