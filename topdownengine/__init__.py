# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

"""pygame-topdownengine is a game engine built on top of the pygame-ce
framework. It allows for the quick creation of 2.5D top-down games."""

from .game import Game
from .game_object import GameObject, GameObjectGroup
from .mobile_object import MobileObject
from .env_object import EnvObject
from .scenes import BaseScene, GameplayScene
from .visual_utils import VisualUtils
from .font import Font
from .camera import Camera, SmoothTrackerCamera
from .asset_paths import PACKAGE_ROOT, ASSETS_DIR

# __version__ attribute
# This only works if the package is installed.
# (E.g. pip install -e .)

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("pygame-topdownengine")
except PackageNotFoundError:
    __version__ = "unknown"

# Clean namespace
del version, PackageNotFoundError