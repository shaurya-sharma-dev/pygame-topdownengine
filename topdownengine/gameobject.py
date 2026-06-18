# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg
from .game import Game
from topdownengine import math as tdg_math
import math

class GameObject(pg.sprite.Sprite):
    SCALE = 50
    SHADOWS = None
    SUBPIXEL = False

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        # Position, Z-Axis, Velocity
        self.position = pg.Vector2()
        self.velocity = pg.Vector2()
        self.elevation = 0
        self.z = 0
        self.z_vel = 0
        self.gravity = 0.01
        self.height = 1

        # Visuals
        self.frame = 0
        self.anim_speed = 0.25
        self.current_animation = 'idle'
        self.obj_shadow = '16x8'
        self.load_animations()
        self.scale_animations()
        if self.SHADOWS is None:
            GameObject.load_and_scale_shadows()
    
    # Visual Methods + Properties
    @classmethod
    def load_and_scale_shadows(cls):
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

        self.animations['idle'] = []
        for i in range(4):
            image = pg.Surface((16, 16))
            image.fill((255/(i+1), 0, 0))
            self.animations['idle'].append(image.convert_alpha())

    def scale_animations(self) -> None:
        "Scale animations."

        for _, anim in self.animations.items():
            for i, frame in enumerate(anim):
                anim[i] = pg.transform.scale(
                    frame,
                    (frame.width * self.SCALE, frame.height * self.SCALE)
                )

    @classmethod
    def set_scale(cls, new_scale: int, game: Game|None):
        cls.SCALE = new_scale
        cls.load_and_scale_shadows()
        if game is None: return
        for go in game.game_object_group:
            go.load_animations()
            go.scale_animations()

    @property
    def image(self) -> pg.Surface:
        "Image for drawing"
        current_anim = self.animations[self.current_animation]
        frame = current_anim[int(self.frame) % len(current_anim)]
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
    def rect(self) -> pg.Rect:
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
    
    # Update
    def update(self, dt: float, game: Game):
        self.z_vel -= self.gravity * dt
        self.z += self.z_vel * dt
        self.z = max(self.z, self.elevation)
        self.frame += self.anim_speed * dt

        # self.position = pg.Vector2(pg.mouse.get_pos())/self.SCALE

        self.position += self.velocity