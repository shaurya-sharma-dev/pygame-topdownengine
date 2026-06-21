# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg

def lerp(start: float|pg.Vector2, end: float|pg.Vector2, t: float) -> float:
    """This function linearly interpolates two floats or Vectors. Accepts t values
    outside of the [0, 1] range. The start and end MUST be the same type.
    
    Args:
        start (float|pg.Vector2): Start Vector2/float
        end (float|pg.Vector2): End Vector2/float
        t (float): Interpolation weight

    Returns: 
        pg.Vector2|float: The interpolated Vector2/float

    Raises:
        TypeError: If `start` and `end` are not the same type.
    """
    if type(start) != type(end):
        raise TypeError(f'{type(start)} and {type(end)} are not the same; they must be equal.')
    return start + (end - start) * t

def scale_rect(rect: pg.Rect|pg.FRect, scalar: int|float) -> pg.Rect|pg.FRect:
    """This function scales a Rect's position and size by a given scalar.
    
    Args:
        rect (pg.Rect|pg.FRect): The Rect object to scale
        scalar (int|float): The number to scale by

    Returns:
        pg.Rect|pg.FRect: The scaled Rect object

    Raises:
        ValueError: If `scalar` <= 0.
    """
    if scalar <= 0:
        raise ValueError('Scalar must be greater than 0.')
    new_rect = rect.copy()
    new_rect.width *= scalar
    new_rect.height *= scalar
    new_rect.top *= scalar
    new_rect.left *= scalar

    return new_rect