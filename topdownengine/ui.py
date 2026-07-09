from __future__ import annotations
import pygame as pg
from collections.abc import Callable
from .font import Font
from .visual_utils import VisualUtils

class UIContainer:
    """Class to store a collection of UI elements.
    
    Attributes:
        elements (set[BaseUIElement]): The set of all elements in this container. This is a managed property.
    """

    def __init__(self):
        "Initialize the UIContainer."
        self._elements = set()

    @property
    def elements(self) -> set[BaseUIElement]:
        "The set of all elements in this container. This is a managed property."
        return self._elements
    
    def add_ui_element(self, element: BaseUIElement) -> None:
        """Add a UI element to this container.
        
        Args:
            element (BaseUIElement): The element to add.

        Raises:
            TypeError: If the element is not an instance of a subclass of BaseUIElement.
        """
        if not isinstance(element, BaseUIElement):
            raise TypeError("Elements must be subclasses of the BaseUIElement class.")
        
        self._elements.add(element)
        element._containers.add(self)

    def remove_ui_element(self, element: BaseUIElement) -> None:
        """Remove a UI element from this container.
        
        Args:
            element (BaseUIElement): The element to remove.
        """
        self._elements.remove(element)
        element._containers.remove(self)

    def remove_all_ui_elements(self) -> None:
        "Remove all UI elements from this container."
        for element in self.elements.copy():
            self.remove_ui_element(element)

    def handle_event(self, event: pg.Event) -> None:
        """Handle a single event for all elements in this container.
        
        Args:
            event (pygame.Event): The event to handle.
        """
        for e in self.elements.copy():
            e.handle_event(event)
    
    def update(self, dt: float) -> None:
        """Update all elements in this container.
        
        Args:
            dt (float): The deltatime.
        """
        for e in self.elements.copy():
            e.update(dt)

    def render(self, surface: pg.Surface) -> None:
        """Render all elementsto a given surface.
        
        Args:
            surface (pygame.Surface): The surface to render to.
        """
        for e in self.elements:
            surface.blit(e.image, e.rect)

class BaseUIElement:
    """Base class for UI elements.
    
    Attributes:
        containers (set[UIContainer]): The set of all containers that contain this element. This is a managed property.
        image (pygame.Surface): The surface of the element. This is a managed property.
    """

    def __init__(self, position: pg.typing.Point, align: str="center", image: pg.Surface=None):
        """Handle a single event for all elements in this container.
        
        Args:
            position (pygame.typing.Point): The position of the element.
            align (str): The alignment of the element.
            image (pygame.Surface, optional): The image to use for the element.
        """
        self._containers = set()
        self._image = image
        if self._image is None:
            self._image = pg.Surface((1,1), pg.SRCALPHA)
        self.rect = self._image.get_rect(**{align: position})
        self.align = align

    @property
    def containers(self) -> set[UIContainer]:
        "The set of all containers that contain this element. This is a managed property."
        return self._containers

    @property
    def image(self) -> pg.Surface:
        "The surface of the element. This is a managed property."
        return self._image
    
    @image.setter
    def image(self, new_image: pg.Surface):
        self._image = new_image
        self.rect = new_image.get_rect(**{self.align: getattr(self.rect, self.align)})

    def add_container(self, container: UIContainer) -> None:
        """Add this UI element to a container.
        
        Args:
            container (UIContainer): The container to add.

        Raises:
            TypeError: If the container is not an instance of UIContainer.
        """

        if not isinstance(container, UIContainer):
            raise TypeError("Containers must be instances of UIContainer.")
        
        self._containers.add(container)
        container._elements.add(self)

    def remove_container(self, container: UIContainer) -> None:
        """Remove this UI element from a container.
        
        Args:
            container (UIContainer): The container to remove from.
        """
        self._containers.remove(container)
        container._elements.remove(self)

    def remove_from_all_containers(self) -> None:
        "Remove this UI element from all containers."
        for container in self.containers.copy():
            self.remove_container(container)

    def handle_event(self, event: pg.Event) -> None:
        """Handle a single event.
        
        Args:
            event (pygame.Event): The event to handle.
        """
        pass
    
    def update(self, dt: float) -> None:
        """Update this element.
        
        Args:
            dt (float): The deltatime.
        """
        pass
    
class Button(BaseUIElement):
    def __init__(self, position: pg.typing.Point, align: str="center", image: pg.Surface=None, on_click: Callable[[], None]=None, hover_highlight_strength: int=100):
        super().__init__(position, align, image)
        self.on_click = on_click
        self.hover_highlight_strength = hover_highlight_strength
        self._enable_hover = False

    def _get_image(self) -> pg.Surface:
        if self._enable_hover and self.is_mouse_over():
            return VisualUtils.make_img_white(self._image, self.hover_highlight_strength)
        
        return self._image
    
    image = property(fget=_get_image, fset=BaseUIElement.image.fset)

    def is_mouse_over(self) -> bool:
        "Is the mouse over this button?"
        return self.rect.collidepoint(pg.mouse.get_pos())
    
    def handle_event(self, event: pg.Event) -> None:
        if event.type == pg.MOUSEBUTTONUP and self.is_mouse_over() and self.on_click is not None:
            self.on_click()

    def update(self, dt: float) -> None:
        self._enable_hover = True

class Text(BaseUIElement):
    def __init__(self, position: pg.typing.Point, font: Font, size: int, text: str, color: pg.typing.ColorLike, align: str="center"):
        image = font._render(size, text, color)
        super().__init__(position, align, image)