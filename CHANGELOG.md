# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/2.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
No current unreleased changes.

## [0.0.1] - 2026-06-19

### Added

- GameObj class to house core systems like drawing image & rect generation, draw index generation, collisions, scaling & rescaling, and shadows.
- MobileObj class (subclass of GameObj) and MobileObjControllers that allows developers to plug in different movement behaviors.
- EnvObj class (subclass of GameObj) that allows adding environmental decorations, collisions, and objects.
- VisualUtils class in order to provide for the easy manipulation of Surfaces.
- Two custom math functions, lerp (that works for Vectors and numbers) and scale_rect, to allow for more concise code.
- KeyboardInputManager class to easily get keyboard input and NoKeysPressed and MoreKeysPressed classes to allow for manipulating the input stream.
- assets/ folder with predefined assets. It currently houses shadows and an example player sprite.