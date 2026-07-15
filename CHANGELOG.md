# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-07-14

### Added
- New `Camera` hook methods `update_screenshake`, `track_game_object`, and `handle_bounds` for easier `Camera` subclassing.
- `SmoothTrackerCamera` subclass of `Camera` for smooth tracking.
- `GameObjectGroup` class to group and update `GameObject` instances together.

### Changed
- **Breaking:** `Game` class to use the `GameObjectGroup` class for `Game.game_object_group` instead of using `pygame.sprite.Group`.
- **Breaking** `GameObject` no longer subclasses `pygame.sprite.Sprite`.

### Fixed
- Bug where the `Game` class would update the camera before updating the active scene. This has been corrected, so now, the active scene is updated, and then the camera.

## [0.4.5] - 2026-07-11

### Fixed
- Bug in `GameObject.update` where it did not use deltatime while moving by `GameObject.velocity`.

## [0.4.4] - 2026-07-09

### Changed
- Performed an internal refactor of `Camera` class.

### Fixed
- Incorrect docstring for the `image` parameter in the `BaseUIElement.__init__` method.
- `Camera` class docstring to state that the `focus_game_object` attribute can be `None`.
- Bug in `Button` class where the `image` would corrupt if the mouse was hovering over it during the first frame.

## [0.4.3] - 2026-07-09

### Fixed
- Added missing return typehint to `Game.set_target_scale`.
- Incorrect formatting for docstrings in the `UIContainer` and `BaseUIElement` classes.
- Resolved a mutable default argument bug in `EnvObject.__init__` that occured with the `colliders` parameter. (See the `EnvObject` entry in 0.4.x documentation.)

## [0.4.2] - 2026-07-08

### Fixed
- Positioning bug in the lighting system.

## [0.4.1] - 2026-07-08

### Fixed
- Build settings to exclude tests, examples, and docs from being added to the wheel.
- `Game.update` to use accumalated deltatime. This ensures that physics are deterministic and prevents bugs in the engine where increased deltatime could break the physics engine.

## [0.4.0] - 2026-07-07

### Added
- `UIContainer.remove_all_ui_elements` method that removes all elements from that UIContainer.
- `BaseUIElement.remove_from_all_containers` method that removes an element from all containers.
- `__version__` string attribute in top-level package namespace.
- The following to the top-level package namespace for easier imports:
    - `BaseScene`
    - `GameplayScene`
    - `Font`
    - `Camera`
    - `PACKAGE_ROOT`
    - `ASSETS_DIR`
- Comprehensive docstrings to the following:
    - `MobileObject` methods
    - Controller classes
    - `Camera` class
    - `KeyboardInputManager`
    - `MoreKeysPressed`
    - `EnvObject`
    - `Font`
    - `GameObject`
    - `Game`
    - `BaseScene`
    - `GameplayScene`
    - `UIContainer`
    - `BaseUIElement`
    - `Button`
    - `VisualUtils`
- `Game.active_scene` managed property that automatically returns the active scene from the `Game.scenes` dictionary.
- `GameObject.light_radius` attribute for new lighting system (see below).
- Lighting system in `GameplayScene` that uses `GameObject.light_radius` to determine light sources.

### Changed
- **Breaking:** `UIContainer.elements` and `BaseUIElement.containers` to managed attributes so that it can no longer be set directly.
- `UIContainer.add_ui_element` to validate elements before adding them to the container.
- `BaseUIElement.add_container` to validate containers before adding the element to them.

### Removed
- **Breaking:** `groups` parameter from the `__init__` methods of `GameObject`, `MobileObject`, and `EnvObject`.

### Fixed
- Docstrings of `topdownengine.math.scale_rect` and `topdownengine.math.lerp` to use "pygame" instead of "pg".
- Return typehint of `topdownengine.math.lerp` to be `pygame.Vector2|float` instead of just `float`.

## [0.3.0] - 2026-07-03

### Added
- New `example-cliff.png` asset to assets folder.
- `Game.bg_color` attribute to control the fill color used in rendering cycles.
- `BaseScene` and `GameplayScene` classes which are used to define scenes, which control the `Game` class's execution loop. For instance, the `GameplayScene` will render and update all `GameObjects` while a different scene could act as the main menu.
- `UIContainer`, `BaseUIElement`, `Button`, and `Text` classes to allow for an object-oriented way to build UIs that are integrated into the engine.

### Changed
- **Breaking:** Rename `GameObject.hitboxes` to `GameObject.world_colliders`.

### Fixed
- `BaseController` class docstring and `StaticController.update` docstring to refer to `MobileObject` instead of `MobileObj` (which was the old name).
- Camera offset in debug rendering logic.

## [0.2.1] - 2026-06-24

### Added
- Dev dependencies (which is currently just `pytest ~= 9.1`).

### Fixed
- Dependencies by using compatible release notation in `pyproject.toml`.

## [0.2.0] - 2026-06-24

### Added
- Docstring to `GameObject` and `GameObject.set_scale`.
- `Game.extra_features` list to be defined upon instantiation that can enable extra features.
- Window resizing logic (you can enable it by appending `"resize"` to `Game.extra_features` when initializing).
- `Camera` class, `Game.camera` attribute that instantiates a `Camera` by default, and camera tracking of `GameObjects`.

### Fixed
- Docstring for `Game` class.

## [0.1.0] - 2026-06-22

### Added
- `Game.debug` boolean attribute which draws the `hitboxes` of all `GameObject` instances in `Game.game_object_group`.

### Changed
- **Breaking:** Renamed `MobileObj` to `MobileObject`.
- **Breaking:** Renamed the `topdownengine.mobile_obj` subpackage to `topdownengine.mobile_object`.
- **Breaking:** Renamed `topdownengine.mobile_object.BaseMobileObjController` to `topdownengine.mobile_obj.BaseController`.
- **Breaking:** Renamed `mobile_obj` parameter in all controller classes to `mobile_object`.

### Removed
- `EnvObject.update` because it was just calling `GameObject.update` and not doing anything else.

### Fixed
- `GameObject.generate_colliders` to divide the default collider's `height` by 2. This makes the collider represent the feet instead of the entire sprite, making the engine more realistic and accurate.

## [0.0.3] - 2026-06-21

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
- `KeyboardInputManager` class to easily get keyboard input and `NoKeysPressed` and `MoreKeysPressed` classes to allow for manipulating the input stream.
- `assets/` folder with predefined assets. It currently houses shadows and an example player sprite.

[unreleased]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.5...v0.5.0
[0.4.5]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.4...v0.4.5
[0.4.4]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.3...v0.4.4
[0.4.3]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.2...v0.4.3
[0.4.2]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.1...v0.4.2
[0.4.1]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/shaurya-sharma-dev/pygame-topdownengine/releases/tag/v0.0.1