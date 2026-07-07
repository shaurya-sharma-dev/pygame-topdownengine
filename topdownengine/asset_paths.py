# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

from pathlib import Path

PACKAGE_ROOT: Path = Path(__file__).resolve().parent
"The folder that represents the root directory of the package."

ASSETS_DIR: Path = PACKAGE_ROOT / "assets"
"The folder that represents the assets directory of the package."