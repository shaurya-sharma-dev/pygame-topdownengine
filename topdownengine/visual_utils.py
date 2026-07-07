# Copyright (c) 2026 Shaurya Sharma
# SPDX-License-Identifier: MIT

import pygame as pg

class VisualUtils:
    @staticmethod
    def load_animation(
        filename: str, 
        frame_width: int, 
        frame_height: int,
        new_frame_width: int=None, 
        new_frame_height: int=None
    ) -> list[pg.Surface]:
        """Loads an animation from a given file with a given frame width and height.
        
        Args:
            filename (str): File path.
            frame_width (int): Frame width.
            frame_height (int): Frame height.
            new_frame_width (int, optional): New frame width. Defaults to None.
            new_frame_height (int, optional): New frame height. Defaults to None.

        Returns: 
            list[pygame.Surface]: The animation.
        """
        sheet = pg.image.load(filename).convert_alpha()
        frames = []
        frame_count = sheet.get_width() // frame_width
        for i in range(frame_count):
            rect = pg.Rect(i * frame_width, 0, frame_width, frame_height)
            frame = pg.transform.scale(sheet.subsurface(rect), (frame_width, frame_height))
            if new_frame_width is not None or new_frame_height is not None:
                frame = pg.transform.scale(frame, (new_frame_width if new_frame_width is not None else frame_width, new_frame_height if new_frame_height is not None else frame_height))
            frames.append(frame)
        return frames

    @staticmethod
    def load_animations(
        filename: str, 
        frame_width: int, 
        frame_height: int, 
        scale_to: int|tuple=None
    ) -> list[list[pg.Surface]]:
        """Loads multiple animations from a given spritesheet with a given frame width and height.
        
        Args:
            filename (str): File path.
            frame_width (int): Frame width.
            frame_height (int): Frame height.
            scale_to (int|tuple, optional): Integer/tuple to scale by/to. Defaults to None.

        Returns: 
            list[list[pygame.Surface]]: The list of animations.
        """
        sheet = pg.image.load(filename).convert_alpha()
        all_rows = []
        
        cols = sheet.get_width() // frame_width
        rows = sheet.get_height() // frame_height
        
        for row in range(rows):
            current_row_frames = []  # Start a new list for this specific row
            for col in range(cols):
                rect = pg.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                if scale_to:
                    if type(scale_to) == int:
                        frame = pg.transform.scale(sheet.subsurface(rect), (rect.width * scale_to, rect.height * scale_to))
                    else:
                        frame = pg.transform.scale(sheet.subsurface(rect), scale_to)
                else:
                    frame = sheet.subsurface(rect)
                current_row_frames.append(frame)
            
            all_rows.append(current_row_frames) # Add the finished row to the master list
                
        return all_rows
    
    @staticmethod
    def flip_animation(
        anim: list[pg.Surface], 
        flip_x: bool=False, 
        flip_y: bool=False
    ) -> list[pg.Surface]:
        """Flip an animation.
        
        Args:
            anim (list[pygame.Surface]): The animation to flip.
            flip_x (bool, optional): Flip x? Defaults to False.
            flip_y (bool, optional): Flip y? Defaults to False.

        Returns: 
            list[pygame.Surface]: The animation.
        """
        new_anim = []
        for frame in anim:
            new_anim.append(
                pg.transform.flip(
                    frame,
                    flip_x,
                    flip_y
                )
            )
        return new_anim

    @staticmethod
    def replace_color(
        surface: pg.Surface, 
        old_color: pg.typing.ColorLike, 
        new_color: pg.typing.ColorLike
    ) -> pg.Surface:
        """Replace all of one given color in a Surface with another.
        
        Args:
            surface (pygame.Surface): The surface to modify.
            old_color (pg.typing.ColorLike): The old color to replace.
            new_color (pg.typing.ColorLike): The new color to replace with.

        Returns: 
            pygame.Surface: The new Surface.
        """
        surface_new = surface.copy()
        with pg.PixelArray(surface_new) as pixels:
            pixels.replace(old_color, new_color)
        return surface_new

    @staticmethod
    def make_img_white(surface: pg.Surface, amount: int=255) -> pg.Surface:
        """Whiten a surface to a given degree.
        
        Args:
            surface (pygame.Surface): The surface to modify.
            amount (int, optional): The degree to whiten by. Defaults to 255.

        Returns: 
            pygame.Surface: The new Surface.
        """
        silhouette = surface.copy()
        silhouette.fill((amount, amount, amount, 0), special_flags=pg.BLEND_RGBA_ADD)
        return silhouette

    @staticmethod
    def draw_low_res_line(
        surface: pg.Surface, 
        color: pg.typing.ColorLike, 
        start_pos: pg.typing.Point, 
        end_pos: pg.typing.Point, 
        res: int=256
    ) -> None:
        """Draw a line that matches the game's pixel resolution.
        
        Args:
            surface (pygame.Surface): The surface to draw the line on.
            color (pygame.typing.ColorLike): The color of the line.
            start_pos (pygame.typing.Point): The start position.
            end_pos (pygame.typing.Point): The end position.
            res (int, optional): The amount to divide by. Defaults to 256.
        """
        sw, sh = surface.get_size()
        if sw > sh:
            lw, lh = res, int(res * (sh / sw))
        else:
            lw, lh = int(res * (sw / sh)), res
            
        low_res_surf = pg.Surface((max(1, lw), max(1, lh)), pg.SRCALPHA)
        scale = sw / lw
        x0, y0 = int(start_pos[0] / scale), int(start_pos[1] / scale)
        x1, y1 = int(end_pos[0] / scale), int(end_pos[1] / scale)
        pg.draw.line(low_res_surf, color, (x0, y0), (x1, y1), 1)
        final_surf = pg.transform.scale(low_res_surf, (sw, sh))
        surface.blit(final_surf, (0, 0))

    @staticmethod
    def create_outline(
        surface: pg.Surface, 
        thickness: int, 
        outline_color: pg.typing.ColorLike
    ) -> pg.Surface:
        """Create an outline of a given thickness and color on a Surface.
        
        Args:
            surface (pygame.Surface): The surface to outline.
            thickness (int): The thickness of the outline.
            outline_color (pygame.typing.ColorLike): The color of the outline.
        """
        mask = pg.mask.from_surface(surface)
        mask_surface = mask.to_surface(setcolor=outline_color)
        mask_surface.set_colorkey((0, 0, 0))
        new_width = surface.get_width() + (thickness * 2)
        new_height = surface.get_height() + (thickness * 2)
        combined_surface = pg.Surface((new_width, new_height), pg.SRCALPHA)
        for dx in range(-thickness, thickness + 1):
            for dy in range(-thickness, thickness + 1):
                if dx == 0 and dy == 0:
                    continue
                if dx**2 + dy**2 <= thickness**2:
                    combined_surface.blit(mask_surface, (dx + thickness, dy + thickness))
                    
        combined_surface.blit(surface, (thickness, thickness))
        return combined_surface