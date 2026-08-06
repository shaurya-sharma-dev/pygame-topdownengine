# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
from topdownengine.ui import UIContainer, BaseUIElement, Button
import pygame as pg
import pytest

class TestUIContainer:
    def test_add_ui_element_method_raises_type_error_if_given_invalid_element(self):
        container = UIContainer()

        with pytest.raises(TypeError, match="Elements must be subclasses of the BaseUIElement class."):
            container.add_ui_element("invalid ui element")

    def test_ui_element_is_in_elements_property_if_added_to_container(self):
        container = UIContainer()
        element = BaseUIElement((0, 0))
        container.add_ui_element(element)
        assert element in container.elements

    def test_ui_element_is_not_in_elements_property_if_removed_from_container(self):
        container = UIContainer()
        element = BaseUIElement((0, 0))
        container.add_ui_element(element)
        container.remove_ui_element(element)
        assert element not in container.elements

    def test_no_ui_elements_in_elements_property_if_all_removed_from_container(self):
        container = UIContainer()
        for _ in range(3):
            element = BaseUIElement((0, 0))
            container.add_ui_element(element)
        container.remove_all_ui_elements()
        assert len(container.elements) == 0

class TestBaseUIElement:
    def test_add_container_method_raises_type_error_if_given_invalid_container(self):
        element = BaseUIElement((0, 0))

        with pytest.raises(TypeError, match="Containers must be instances of UIContainer."):
            element.add_container("invalid container")

    def test_ui_container_is_in_containers_property_if_added_to_element(self):
        container = UIContainer()
        element = BaseUIElement((0, 0))
        element.add_container(container)
        assert container in element.containers

    def test_ui_container_is_not_in_containers_property_if_removed_from_element(self):
        container = UIContainer()
        element = BaseUIElement((0, 0))
        element.add_container(container)
        element.remove_container(container)
        assert container not in element.containers

    def test_no_ui_containers_in_containers_property_if_all_removed_from_element(self):
        element = BaseUIElement((0, 0))
        for _ in range(3):
            container = UIContainer()
            element.add_container(container)
        element.remove_from_all_containers()
        assert len(element.containers) == 0

    def test_image_is_set_and_alignment_is_constant_if_image_property_is_set(self):
        element = BaseUIElement((0, 0))
        element.image = pg.Surface((100, 100))

        assert element.image is element.image
        assert element.rect.center == (0, 0)

class TestButton:
    def test_on_click_is_called_if_mousebuttonup_event_sent_while_mouse_over(self, monkeypatch):
        button = Button((0, 0), "topleft", pg.Surface((100, 100)), lambda: setattr(button, "clicked", True))
        button.clicked = False

        event = pg.Event(pg.MOUSEBUTTONUP, dict())

        monkeypatch.setattr(pg.mouse, "get_pos", lambda: (50, 50))
        button.handle_event(event)

        assert button.clicked

    def test_on_click_is_not_called_if_mousebuttonup_event_sent_while_mouse_not_over(self, monkeypatch):
        button = Button((0, 0), "topleft", pg.Surface((100, 100)), lambda: setattr(button, "clicked", True))
        button.clicked = False

        event = pg.Event(pg.MOUSEBUTTONUP, dict())

        monkeypatch.setattr(pg.mouse, "get_pos", lambda: (150, 50))
        button.handle_event(event)

        assert not button.clicked

    def test_image_is_highlighted_if_mouse_over_after_first_frame(self, monkeypatch, game):
        image = pg.Surface((100, 100), pg.SRCALPHA)
        image.fill("black")

        button = Button((0, 0), "topleft", image)
        button.update(0) # "Complete" first frame.
        
        monkeypatch.setattr(pg.mouse, "get_pos", lambda: (50, 50))
        manually_highlighted = tde.VisualUtils.make_img_white(image, button.hover_highlight_strength).convert_alpha()

        assert pg.image.tobytes(button.image, "RGBA") == pg.image.tobytes(manually_highlighted, "RGBA")

    def test_image_is_not_highlighted_if_mouse_over_during_first_frame(self, monkeypatch, game):
        image = pg.Surface((100, 100), pg.SRCALPHA)
        image.fill("black")

        button = Button((0, 0), "topleft", image)
        
        monkeypatch.setattr(pg.mouse, "get_pos", lambda: (50, 50))
        manually_highlighted = tde.VisualUtils.make_img_white(button._image, button.hover_highlight_strength).convert_alpha()

        assert pg.image.tobytes(button.image, "RGBA") != pg.image.tobytes(manually_highlighted, "RGBA")
        assert pg.image.tobytes(button.image, "RGBA") == pg.image.tobytes(image, "RGBA")

    def test_image_is_not_highlighted_if_mouse_not_over(self, monkeypatch, game):
        image = pg.Surface((100, 100), pg.SRCALPHA)
        image.fill("black")

        button = Button((0, 0), "topleft", image)
        button.update(0) # "Complete" first frame.
        
        monkeypatch.setattr(pg.mouse, "get_pos", lambda: (150, 50))
        manually_highlighted = tde.VisualUtils.make_img_white(image, button.hover_highlight_strength).convert_alpha()

        assert pg.image.tobytes(button.image, "RGBA") != pg.image.tobytes(manually_highlighted, "RGBA")