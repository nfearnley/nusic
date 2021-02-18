import pygame
import pygame.draw
from pygame.font import SysFont

from nusic.constants import TRANS
from nusic.controls import Button, Progress, Text
from nusic.controls.control import Control
from nusic.music import music


class Background(Control):
    def __init__(self, game, size):
        super().__init__()
        self.game = game
        self.image = pygame.Surface(size)
        self.drag_from = None
        self.draw()

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.end_drag()
        self.update_drag()
        super().update(events)

    def draw(self):
        self.image.fill(TRANS)
        pygame.draw.rect(self.image, "#331111", self.rect, border_radius=40)
        pygame.draw.rect(self.image, "#551111", self.rect, width=5, border_radius=40)

    def on_mousedown(self, mousexy):
        self.begin_drag()

    def begin_drag(self):
        self.drag_from = self.game.screenmouse, self.game.position

    def end_drag(self):
        self.drag_from = None

    def update_drag(self):
        if self.drag_from is None:
            return
        tox, toy = self.game.screenmouse
        (fromx, fromy), (oldx, oldy) = self.drag_from
        diffx, diffy = tox - fromx, toy - fromy
        self.game.position = oldx + diffx, oldy + diffy


class PlayButton(Button):
    def __init__(self):
        super().__init__("▶", pos=(300 - 100 - 15, 122), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.play()


class PauseButton(Button):
    def __init__(self):
        super().__init__("⏸", pos=(300 - 60 - 15, 120), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.pause()


class PlayPauseButton(Button):
    def __init__(self):
        super().__init__("⏯", pos=(300 - 20 - 15, 120), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.playpause()


class StopButton(Button):
    def __init__(self):
        super().__init__("⏹", pos=(300 + 20 - 15, 122), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.stop()


class RWButton(Button):
    def __init__(self):
        super().__init__("⏮", pos=(300 + 60 - 15, 120), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.elapsed -= 5


class FFButton(Button):
    def __init__(self):
        super().__init__("⏭", pos=(300 + 100 - 15, 120), size=(30, 30))

    def on_mousedown(self, mousexy):
        super().on_mousedown(mousexy)
        music.elapsed += 5


class MusicPlayer:
    def __init__(self, game):
        self.game = game
        self.size = (600, 200)
        self.surface = pygame.Surface(self.size)
        self.surface.set_colorkey(TRANS)

        music.load("girltower.ogg")

        # icons = "⏵▶▶️⏸⏸️⏯⏯️◀◀️⏹⏹️⏪⏪️⏩⏩️⏮⏮️⏭⏭️⏺⏺️⏏⏏️🔀🔀️🔁🔁️🔃🔃️🔂🔂️ℹℹ️🔄🔄️"

        self.background = Background(game, self.size)
        self.progressbar = Progress((50, 160), (500, 25), val=music.elapsed, maxval=music.length)
        self.elapsed_text = Text(pos=(50, 140), font=SysFont("Lato", 12, bold=True))
        self.remaining_text = Text(pos=(500, 140), font=SysFont("Lato", 12, bold=True))
        self.status_text = Text(pos=(240, 50), font=SysFont("Lato", 36, bold=True))
        self.play_button = PlayButton()
        self.pause_button = PauseButton()
        self.playpause_button = PlayPauseButton()
        self.stop_button = StopButton()
        self.rw_button = RWButton()
        self.ff_button = FFButton()

        self.controls = pygame.sprite.LayeredUpdates()
        self.controls.add(self.background, layer=0)
        self.controls.add(self.progressbar, layer=1)
        self.controls.add(self.elapsed_text, layer=1)
        self.controls.add(self.remaining_text, layer=1)
        self.controls.add(self.status_text, layer=1)
        self.controls.add(self.play_button, layer=1)
        self.controls.add(self.pause_button, layer=1)
        self.controls.add(self.playpause_button, layer=1)
        self.controls.add(self.stop_button, layer=1)
        self.controls.add(self.rw_button, layer=1)
        self.controls.add(self.ff_button, layer=1)

        music.volume = 0.2
        music.play()

    def get_control_at(self, xy):
        try:
            return self.controls.get_sprites_at(xy)[-1]
        except IndexError:
            return None

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                mousexy = pygame.mouse.get_pos()
                ctrl = self.get_control_at(mousexy)
                self.trigger(ctrl, "on_mouseup", mousexy)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousexy = pygame.mouse.get_pos()
                ctrl = self.get_control_at(mousexy)
                self.trigger(ctrl, "on_mousedown", mousexy)

        self.elapsed_text.text = f"{nice_time(music.elapsed, show='ms', precision=2)} / {nice_time(music.length, show='ms')}"
        self.remaining_text.text = f"{nice_time(music.remaining, show='ms', precision=2)}"
        self.status_text.text = f"{music.status.value}"
        self.progressbar.val = music.elapsed
        self.controls.update(events)

    def draw(self):
        self.controls.draw(self.surface)
        return self.surface

    def trigger(self, ctrl, name, *args, **kwargs):
        if ctrl is None:
            return
        try:
            event = getattr(ctrl, name)
        except AttributeError:
            event = None
        if event is not None and callable(event):
            event(*args, **kwargs)


def nice_time(seconds: float, show="hms", precision=0):
    if sorted(show) == "hs":
        raise ValueError(f"{show!r} is an invalid show value")
    h = int(seconds / 3600)
    m = int(seconds / 60)
    s = seconds

    # get top value
    top = None
    if "h" in show:
        top = "h"
    elif "m" in show:
        top = "m"
    elif "s" in show:
        top = "s"

    if "h" in show:
        m %= 60
    if "m" in show:
        s, frac = divmod(s, 1)
        s %= 60
        s += frac

    out = []
    if "h" in show:
        out.append(str(h))
    if "m" in show:
        if top == "m":
            out.append(str(m))
        else:
            out.append(format(m, "02"))
    if "s" in show:
        if top == "s":
            out.append(str(s))
        else:
            if precision:
                pad = 3 + precision
            else:
                pad = 2
            precmul = (10 ** precision)
            s = int(s * precmul) / precmul  # chop off unnecessary digits
            out.append(format(s, f"0{pad}.{precision}f"))
    return ":".join(out)
