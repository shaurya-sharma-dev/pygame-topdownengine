# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
from .game import Game
from .visual_utils import VisualUtils
from topdownengine import math as tde_math

class GameObject(pg.sprite.Sprite):
    SCALE = 1
    SHADOWS = None
    SUBPIXEL = False
    VELOCITY_DEADZONE = 0.2

    def __init__(self, *groups: pg.sprite.Group) -> None:
        super().__init__(*groups)

        # Position, Z-Axis, Velocity
        self.position = pg.Vector2()
        self.velocity = pg.Vector2()
        self.elevation = 0
        self.z = 0
        self.z_vel = 0
        self.gravity = 0.005
        self.height = 8

        # Visuals
        self.frame = 0
        self.anim_speed = 0.25
        if getattr(self, 'animation_paths', None) is not None:
            self.current_animation = list(self.animation_paths.keys())[0]
        else:
            self.current_animation = 'idle'
        self.obj_shadow = '16x8'
        self.load_animations()
        self.scale_animations()
        if self.SHADOWS is None:
            GameObject.load_and_scale_shadows()

        self.colliders = self.generate_colliders()
    
    # Visual Methods + Properties
    @classmethod
    def load_and_scale_shadows(cls) -> None:
        from topdownengine.asset_paths import ASSETS_DIR
        shadows = list((ASSETS_DIR / "shadows").glob("*.png"))
        cls.SHADOWS = dict()
        for shadow in shadows:
            shadow_img = pg.image.load(
                shadow
            ).convert_alpha()

            cls.SHADOWS[shadow.name.replace('.png', '')] = pg.transform.scale(
                shadow_img,
                (shadow_img.width * cls.SCALE, shadow_img.height * cls.SCALE)
            )

    def load_animations(self) -> None:
        "Load unscaled animations."
        self.animations = dict()

        if getattr(self, 'animation_paths', None) is None:
            # When there is no animation path data, add red
            # square idle animation with changing colors.
            self.animations['idle'] = []
            for i in range(4):
                image = pg.Surface(getattr(self, 'frame_size', (16, 16)))
                image.fill((255/(i+1), 0, 0))
                self.animations['idle'].append(image.convert_alpha())
        else:
            for k, v in self.animation_paths.items():
                if getattr(self, 'directional_anims', False):
                    dirs = ['d', 'r', 'u', 'l']
                    all_anims = VisualUtils.load_animations(v, *self.frame_size)
                    all_anims.append(VisualUtils.flip_animation(all_anims[1], True, False))
                    for i, anim in enumerate(all_anims):
                        self.animations[f'{k}_{dirs[i]}'] = anim

                else:
                    self.animations[k] = VisualUtils.load_animation(v, *self.frame_size)

    def scale_animations(self) -> None:
        "Scale animations."
        for _, anim in self.animations.items():
            for i, frame in enumerate(anim):
                anim[i] = pg.transform.scale(
                    frame,
                    (frame.width * self.SCALE, frame.height * self.SCALE)
                )

    @classmethod
    def set_scale(cls, new_scale: int, game: Game|None) -> None:
        cls.SCALE = new_scale
        cls.load_and_scale_shadows()
        if game is None: return
        for go in game.game_object_group:
            go.load_animations()
            go.scale_animations()

    @property
    def current_frame(self) -> pg.Surface:
        "Current animation frame the GameObj is on."
        if getattr(self, 'directional_anims', False):
            current_anim = self.animations[f"{self.current_animation}_{self.current_dir}"]
        else:
            current_anim = self.animations[self.current_animation]
        return current_anim[int(self.frame) % len(current_anim)]

    @property
    def image(self) -> pg.Surface:
        "Image for drawing."
        frame = self.current_frame
        shadow = None
        if self.obj_shadow is not None:
            shadow = self.SHADOWS[self.obj_shadow]

        if self.SUBPIXEL:
            z_elevation_offset = (self.z - self.elevation) * self.SCALE
        else:
            z_elevation_offset = int(self.z - self.elevation) * self.SCALE
        image = pg.Surface(
            (
                frame.width, 
                (frame.height + z_elevation_offset + 
                (shadow.height//2 if shadow is not None else 0))
            ), 
            pg.SRCALPHA
        )
        if shadow is not None: image.blit(shadow, (0, image.height - shadow.height))
        image.blit(frame, (0, 0))
        return image
        
    @property
    def rect(self) -> pg.Rect|pg.FRect:
        "Rect object for drawing."
        shadow_offset = pg.Vector2(0, self.SHADOWS[self.obj_shadow].height//2 if self.obj_shadow is not None else 0)
        elev_pos = self.position - pg.Vector2(0, self.elevation)
        if self.SUBPIXEL:
            return self.image.get_frect(
                midbottom=elev_pos * self.SCALE + shadow_offset
            )

        elev_pos.x = int(elev_pos.x)
        elev_pos.y = int(elev_pos.y)
        return self.image.get_rect(
            midbottom=elev_pos * self.SCALE + shadow_offset
        )
    
    @property
    def draw_index(self) -> int:
        return (self.z, self.rect.bottom)
    
    # Collisions
    def generate_colliders(self) -> list[pg.Rect|pg.FRect]:
        "Default list of Rect objects for collisions."
        frame = self.current_frame
        elev_pos = self.position - pg.Vector2(0, self.elevation)
        if self.SUBPIXEL:
            r = self.current_frame.get_frect(
                topleft=elev_pos * self.SCALE
            )
        else:
            elev_pos.x = int(elev_pos.x)
            elev_pos.y = int(elev_pos.y)
            r = self.current_frame.get_rect(
                topleft=elev_pos * self.SCALE
            )

        r = tde_math.scale_rect(r, 1/self.SCALE)

        return [r]
    
    @property
    def hitboxes(self) -> list[pg.Rect]:
        """Return a list of hitbox Rects in world-space, as opposed to
        GameObj.colliders, which uses relative positioning to the
        GameObj itself."""
        return [
            pg.Rect(c.left + self.position.x - c.width//2, c.top + self.position.y - c.height - self.elevation, c.width, c.height)
            for c in self.colliders
        ]
    
    @property
    def unelevated_hitboxes(self) -> list[pg.Rect]:
        """Return a list of hitbox Rects in world-space unelevated, as opposed to
        GameObj.colliders, which uses relative positioning to the
        GameObj itself."""
        return [
            pg.Rect(c.left + self.position.x - c.width//2, c.top + self.position.y - c.height, c.width, c.height)
            for c in self.colliders
        ]

    def _handle_collision(self, dir: pg.Vector2, game: Game) -> bool:
        """Checks for collisions and moves the GameObj. Returns whether a collision occured or not."""
        if dir.x and dir.y:
            raise ValueError('Both axes cannot be moved in one step. Move them in separate method calls.')
        
        moving_right = dir.x > 0
        moving_down = dir.y > 0
        moving_x = bool(dir.x)

        self.position += dir

        collision_found = True
        return_value = False
        while collision_found:
            collision_found = False
            for self_hitbox in self.hitboxes:  # always fresh
                for game_obj in game.game_object_group:
                    if game_obj is self or (game_obj.z + game_obj.height) <= self.z:
                        continue
                    for other_hitbox in game_obj.hitboxes:
                        if self_hitbox.colliderect(other_hitbox):
                            if moving_x:
                                if moving_right:
                                    self.position.x += other_hitbox.left - self_hitbox.right
                                else:
                                    self.position.x += other_hitbox.right - self_hitbox.left
                            else:
                                if moving_down:
                                    self.position.y += other_hitbox.top - self_hitbox.bottom
                                else:
                                    self.position.y += other_hitbox.bottom - self_hitbox.top
                            collision_found = True
                            return_value = True
                            break  # restart with fresh hitboxes
                    if collision_found:
                        break
                if collision_found:
                    break

        return return_value

    def _handle_elevation(self, game: Game) -> None:
        new_elevation = 0

        for self_hitbox in self.hitboxes:
            for game_obj in game.game_object_group:
                if game_obj is self:
                    continue

                for other_hitbox in game_obj.hitboxes:
                    if self_hitbox.colliderect(other_hitbox) or self.unelevated_hitboxes[self.hitboxes.index(self_hitbox)].colliderect(other_hitbox):
                        new_elevation = max(new_elevation, game_obj.height + game_obj.elevation)

        self.elevation = new_elevation

    # Update
    def update(self, dt: float, game: Game) -> None:
        # Gravity
        self.z_vel -= self.gravity * dt
        self.z += self.z_vel * dt
        self.z = max(self.z, self.elevation)

        # Frame Update
        self.frame += self.anim_speed * dt

        # Add Velocity To Position
        if self.velocity.length() <= self.VELOCITY_DEADZONE:
            # Add a 'deadzone' where if the velocity is low enough, it just becomes (0, 0)
            self.velocity = pg.Vector2()

        if not self.velocity.length():
            return
        
        self._handle_collision(pg.Vector2(self.velocity.x, 0), game)
        self._handle_collision(pg.Vector2(0, self.velocity.y), game)
        self._handle_elevation(game)