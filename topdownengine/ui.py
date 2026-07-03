from __future__ import annotations
import pygame as pg
from collections.abc import Callable
from .font import Font

class UIContainer:
    def __init__(self):
        self.elements = set()
    
    def add_ui_element(self, element: BaseUIElement) -> None:
        self.elements.add(element)
        element.containers.add(self)

    def remove_ui_element(self, element: BaseUIElement) -> None:
        self.elements.remove(element)
        element.containers.remove(self)

    def handle_event(self, event: pg.Event) -> None:
        for e in self.elements:
            e.handle_event(event)
    
    def update(self, dt: float) -> None:
        for e in self.elements:
            e.update(dt)

    def render(self, surface: pg.Surface) -> None:
        for e in self.elements:
            surface.blit(e.image, e.rect)

class BaseUIElement:
    def __init__(self, position: pg.typing.Point, align: str="center", image: pg.Surface=None):
        self.containers = set()
        self._image = image
        if self._image is None:
            self._image = pg.Surface((1,1), pg.SRCALPHA)
        self.rect = self._image.get_rect(**{align: position})
        self.align = align

    @property
    def image(self) -> pg.Surface:
        return self._image
    
    @image.setter
    def image(self, new_image: pg.Surface):
        self._image = new_image
        self.rect = new_image.get_rect(**{self.align: getattr(self.rect, self.align)})

    def add_container(self, container: UIContainer) -> None:
        self.containers.add(container)
        container.elements.add(self)

    def remove_container(self, container: UIContainer) -> None:
        self.containers.remove(container)
        container.elements.remove(self)

    def handle_event(self, event: pg.Event) -> None:
        pass
    
    def update(self, dt: float) -> None:
        pass

class Button(BaseUIElement):
    def __init__(self, position: pg.typing.Point, align: str="center", image: pg.Surface=None, on_click: Callable[[], None]=None, hover_highlight_strength: int=100):
        super().__init__(position, align, image)
        self.on_click = on_click
        self.hover_highlight_strength = hover_highlight_strength

    def _get_image(self) -> pg.Surface:
        if self.is_mouse_over():
            highlighted_image = self._image.copy()
            highlighted_image.fill(
                (self.hover_highlight_strength, self.hover_highlight_strength, self.hover_highlight_strength, 0), 
                special_flags=pg.BLEND_RGBA_ADD
            )
            return highlighted_image
        
        return self._image
    
    image = property(fget=_get_image, fset=BaseUIElement.image.fset)

    def is_mouse_over(self) -> bool:
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def handle_event(self, event: pg.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and self.is_mouse_over() and self.on_click is not None:
            self.on_click()

class Text(BaseUIElement):
    def __init__(self, position: pg.typing.Point, font: Font, size: int, text: str, color: pg.typing.ColorLike, align: str="center"):
        image = font._render(size, text, color)
        super().__init__(position, align, image)