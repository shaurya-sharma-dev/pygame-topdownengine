# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Google-style docstrings to `MobileObj`, `scale_rect`, `lerp`, `KeyboardInputController`, and `MoreKeysPressed`.

### Changed
- Internal logic of `GameObject.generate_colliders` to remove unused `frame` variable.
- `KeyboardInputManager` so that `KeyboardInputManager.keys` and `KeyboardInputManager.just_pressed_keys` are no longer defined in `__init__`.

### Fixed
- `MobileObj` to make the angles required for up and down animations narrower (45 degrees each) and left and right wider (135 degrees each).
- `GameObject.draw_index` to use `GameObject.elevation` instead of `GameObject.z`.

## [0.0.2] - 2026-06-20

### Fixed
- Elevation detection by no longer using `GameObject.unelevated_hitboxes`.

### Removed 
- **Breaking:** `GameObject.unelevated_hitboxes`.

## [0.0.1] - 2026-06-19

### Added

- `GameObject` class to house core systems like drawing image & rect generation, draw index generation, collisions, scaling & rescaling, and shadows.
- `MobileObj` class (subclass of `GameObject`) and `MobileObjControllers` that allows developers to plug in different movement behaviors.
- `EnvObject` class (subclass of `GameObject`) that allows adding environmental decorations, collisions, and objects.
- `VisualUtils` class in order to provide for the easy manipulation of Surfaces.
- Two custom math functions, `lerp` (that works for Vectors and numbers) and `scale_rect`, to allow for more concise code.
- `KeyboardInputManager` class to easily get keyboard input and NoKeysPressed and MoreKeysPressed classes to allow for manipulating the input stream.
- `assets/` folder with predefined assets. It currently houses shadows and an example player sprite.