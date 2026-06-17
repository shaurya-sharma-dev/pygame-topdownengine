import pygame as pg

def lerp(start: float|pg.Vector2, end: float|pg.Vector2, t: float) -> float:
    """This function linearly interpolates two floats or Vectors. Accepts t values
    outside of the [0, 1] range. The start and end MUST be the same type.
    
    Keyword arguments:
    start -- Start Vector/float
    end -- End Vector/float
    t -- Interpolation weight
    Return: New Vector/float
    """
    if type(start) != type(end):
        raise TypeError(f'{type(start)} and {type(end)} are not the same; they must be equal.')
    return start + (end - start) * t