# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import topdownengine as tde
from topdownengine.ui import UIContainer, BaseUIElement
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