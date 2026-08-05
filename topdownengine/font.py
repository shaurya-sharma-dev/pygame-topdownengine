import pygame as pg

class Font:
    """A class built on top of pygame.Font that allows for caching of different sizes, prebuilt word wrap, and other features.
        
    Attributes:
        path (str): The path to load from. If there is no font at that path, it will load a system font of that name.
    """

    def __init__(self, path: str):
        """Initialize the Font object.
        
        Args:
            path (str): The path to load from. If there is no font at that path, it will load a system font of that name.
        """
        
        self.path = path
        self._sizes = {}

    def _get_size(self, size: int) -> pg.Font:
        if not size in self._sizes: 
            try:
                # Attempt to load it as a custom font file
                self._sizes[size] = pg.font.Font(self.path, size)
            except (FileNotFoundError, pg.error):
                # Try to get it as a system font if it doesn't exist
                # If it's not a system font, pygame-ce uses a default font.
                self._sizes[size] = pg.font.SysFont(self.path, size)

        return self._sizes[size]

    def get_max_size_for_text_in_rect(self, text: str, target_rect: pg.Rect):
        """Finds the largest font size where the text fits inside a target_rect. Uses the height as the maximum logical starting size.
        
        Args:
            text (str): The text to scale.
            target_rect (pygame.Rect): The Rect object to scale to.
        
        Returns:
            int: The largest possible font size where the text fits in the target_rect.
        """
        start_size = max(2, target_rect.height)

        for size in range(start_size, 1, -1):
            rendered = self._render(size, text, "black")
            text_w, text_h = rendered.get_bounding_rect().size
            
            if text_w <= target_rect.width and text_h <= target_rect.height:
                return size
                
        return 2
    
    def wrap(self, line: str, size: int, max_width: int) -> list[str]:
        """Break a single string into multiple lines based on width.
        
        Args:
            line (str): The string to wrap.
            size (int): The fontsize to use for calculations.
            max_width (int): The maximum width for each wrapped line.
            
        Returns:
            list[str]: The list of wrapped lines.
        """
        lines = []
        current_line = ""
        fnt = self._get_size(size)
        
        # Split by spaces
        words = line.split(" ")

        for word in words:
            if not word: 
                continue
            
            # Determine the line to test size with
            test_line = f"{current_line} {word}" if current_line else word

            # If it fits, add it to the current line
            if fnt.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                # The current line is full, so append it and make a new line.
                if current_line:
                    lines.append(current_line)
                    current_line = ""

                # Check if the word itself is wider than max_width
                if fnt.size(word)[0] > max_width:
                    # Split by character for oversized words
                    temp_word = ""
                    for char in word:
                        if fnt.size(temp_word + char)[0] <= max_width:
                            temp_word += char
                        else:
                            lines.append(temp_word)
                            temp_word = char
                    current_line = temp_word
                else:
                    current_line = word

        # Add the final leftover line
        if current_line:
            lines.append(current_line)

        return lines

    def _render(self, size: int, text: str, color: pg.typing.ColorLike):
        return self._get_size(size).render(text, True, color)

    def draw_text(self, text: str, x: int, y: int, size: int, surface: pg.Surface, color: pg.typing.ColorLike, align: str="center") -> None:
        """Draws text to a surface.
        
        Args:
            text (str): The text to render to the surface.
            x (int): The x-position.
            y (int): The y-position.
            size (int): The font size to use.
            surface (pygame.Surface): The surface to render to.
            color (pygame.typing.ColorLike): The color to use.
            align (str): The alignment to use. Defaults to "center".
            
        Raises:
            ValueError: If an invalid align argument is passed into the method.
        """
        surf = self._render(size, text, color)

        try:
            rect = surf.get_rect(**{align: (x, y)})
        except AttributeError:
            raise ValueError(f"Invalid align value of {align}")
        
        surface.blit(surf, rect)