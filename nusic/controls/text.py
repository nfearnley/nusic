
from .control import Control, uses
from pygame.font import SysFont


class Text(Control):
    def __init__(self, text="", *, pos=(0, 0), font=None, color="#DD3333"):
        super().__init__(pos)
        self.text = text
        if font is None:
            font = SysFont("Lato", 18, bold=True)
        self.font = font
        self.color = color

        self.image = None
        self.draw()

    @uses("text", "color", "font")
    def draw(self):
        self.image = self.font.render(self.text, True, self.color)
