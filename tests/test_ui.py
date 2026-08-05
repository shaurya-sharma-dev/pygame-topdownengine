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

class TestBaseUIElement:
    def test_add_container_method_raises_type_error_if_given_invalid_container(self):
        element = BaseUIElement((0, 0))

        with pytest.raises(TypeError, match="Containers must be instances of UIContainer."):
            element.add_container("invalid container")