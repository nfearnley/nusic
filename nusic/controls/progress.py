from nusic.controls.control import Control, uses
import pygame.draw

from nusic.constants import TRANS
from nusic.music import music


class Progress(Control):
    def __init__(self, pos, size, *, val=0, minval=0, maxval=1, bar_color="#550000", slider_color="#AA2222"):
        super().__init__(pos)
        self.size = size
        self.val = val
        self.minval = minval
        self.maxval = maxval
        self.bar_color = bar_color
        self.slider_color = slider_color
        self.image = None
        self.drag_from = None
        self.slider_rect = None

        self.draw()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.end_drag()
        if self.drag_from:
            bar_width = (self.image.get_rect().width - 20)
            (oldx, oldy), oldval = self.drag_from
            newx, newy = pygame.mouse.get_pos()
            diffx = newx - oldx
            newval = oldval + ((diffx / bar_width) * (self.maxval - self.minval))
            music.elapsed = newval
        super().update(events)

    def on_mousedown(self, mousexy):
        x, y = mousexy[0] - self.pos[0], mousexy[1] - self.pos[1]
        if self.slider_rect.collidepoint((x, y)):
            self.begin_drag(mousexy)

    def begin_drag(self, mousexy):
        self.drag_from = mousexy, self.val

    def end_drag(self):
        self.drag_from = None

    @uses("size", "val", "minval", "maxval", "bar_color", "slider_color")
    def draw(self):
        self.image = pygame.Surface(self.size)
        self.image.set_colorkey(TRANS)
        self.image.fill(TRANS)
        rect = self.image.get_rect()
        progress = (self.val - self.minval) / (self.maxval - self.minval)
        self.slider_rect = rect.copy()
        self.slider_rect.width = 10
        self.slider_rect.centerx = 10 + (progress * (rect.width - 20))
        bar_rect = rect.copy()
        bar_rect.w -= 20
        bar_rect.centerx = rect.centerx
        pygame.draw.line(self.image, self.bar_color, bar_rect.midleft, bar_rect.midright, width=2)
        pygame.draw.rect(self.image, self.slider_color, self.slider_rect)
