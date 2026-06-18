import pygame as pg

class VisualUtils:
    @staticmethod
    def load_animation(filename, frame_width, frame_height, new_frame_width=None, new_frame_height=None):
        "Loads an animation from a given file with a given frame width and height"
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
    def load_animations(filename, frame_width, frame_height, scale_to: int|tuple=None) -> list[list[pg.Surface]]:
        "Loads multiple animations from a given spritesheet with a given frame width and height."
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
    def flip_animation(anim: list[pg.Surface], flip_x: bool=False, flip_y: bool=False):
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
        "Replace all of one given color in a Surface with another."
        surface_new = surface.copy()
        with pg.PixelArray(surface_new) as pixels:
            pixels.replace(old_color, new_color)
        return surface_new

    @staticmethod
    def make_img_white(surface: pg.Surface, amount: int=255):
        "Make a Surface white to a given degree (defaults to 255)."
        silhouette = surface.copy()
        silhouette.fill((amount, amount, amount, 0), special_flags=pg.BLEND_RGBA_ADD)
        return silhouette

    @staticmethod
    def draw_low_res_line(screen, color, start_pos, end_pos, res=256):
        "Draw a line that matches the game's pixel resolution."
        sw, sh = screen.get_size()
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
        screen.blit(final_surf, (0, 0))

    @staticmethod
    def create_outline(
        surface: pg.Surface, 
        thickness: int, 
        outline_color: pg.typing.ColorLike
    ) -> pg.Surface:
        "Create an outline of a given thickness and color on a Surface."
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