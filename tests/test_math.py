# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from topdownengine import math as tde_math
import pytest

LERP_TEST_ARGS = [
    [5, 8], # P->P
    [1, -7], # P->N
    [5, 0], # P->0
    [-8, 5], # N->P
    [-5, -10], # N->N
    [-7, 0], # N->0
    [0, 7], # 0->P
    [0, -6], # 0->N
    [0, 0], # 0->0
]

@pytest.mark.parametrize("start, end", LERP_TEST_ARGS)
def test_lerp_with_t_0_equals_start(start, end):
    assert tde_math.lerp(start, end, 0) == start

@pytest.mark.parametrize("start, end", LERP_TEST_ARGS)
def test_lerp_with_t_1_equals_end(start, end):
    assert tde_math.lerp(start, end, 1) == end