from nusic.constants import TRANS
import pygame
from pygame.font import SysFont
from .control import Control, uses


class Button(Control):
    def __init__(self, text="", *, pos=(0, 0), size=(0, 0), font=None, color="#AA2222", pressed_color="#EE2222"):
        super().__init__(pos)
        self.size = size
        self.text = text
        if font is None:
            font = SysFont("Segoe UI Symbol", size[0])
        self.font = font
        self.color = color
        self.pressed_color = pressed_color
        self.pressed = False

        self.image = None
        self.draw()

    @property
    def rect(self):
        return self.image.get_rect().move(*self.pos)

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.pressed = False
        super().update(events)

    def on_mousedown(self, mousexy):
        self.pressed = True

    @uses("size", "text", "color", "font", "pressed")
    def draw(self):
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey(TRANS)
        self.image.fill(TRANS)
        color = self.pressed_color if self.pressed else self.color
        text = self.font.render(self.text, False, color)
        dest_rect = text.get_rect()
        dest_rect.center = self.image.get_rect().center
        self.image.blit(text, dest_rect)
