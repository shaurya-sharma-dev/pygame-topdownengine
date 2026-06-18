# pygame-topdownengine
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](https://opensource.org)

pygame-topdownengine is a 2.5D engine for top-down games. It is designed to be highly modular, with most core systems being located in the easily extendible GameObject class. It is built on top of the pygame-ce package, which you can find here: https://github.com/pygame-community/pygame-ce/tree/main.

## Features
- GameObject class that contains all of the core systems.
- Built-in Mob class for anything that moves.
- Option to use either pixel-perfect or subpixel rendering.
- Dynamic scale-setting for all GameObjects.
- Robust 3D collision detection.

## Installation
In order to install pygame-topdownengine, make sure Python and pip are both installed and in PATH. Then, run this command into your terminal:
`pip install pygame-topdownengine`
NOTE: THE PACKAGE IS NOT ON PYPI YET, SO THE COMMAND WILL NOT WORK.

## License
This library is distributed under the MIT license, which can be found in the root of this repository under the `LICENSE` file.

The files located in the `examples` folder are licensed under the Creative Commons Zero 1.0 Universal license, which can be found inside of `examples/LICENSE`.