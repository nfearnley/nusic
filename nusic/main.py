from nusic.player import MusicPlayer
import win32gui
import win32con
import win32api

from pygame._sdl2.video import Window
import pygame
import pygame.freetype

from nusic.constants import TRANS


# Hacks to make window see-thru
def seethru():
    transcolor = pygame.Color(TRANS)
    wintranscolor = win32api.RGB(transcolor.r, transcolor.g, transcolor.b)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, wintranscolor, 0, win32con.LWA_COLORKEY)


class Game:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.player = MusicPlayer(self)
        self.screen = pygame.display.set_mode(self.player.size, pygame.NOFRAME)
        seethru()
        self.window = Window.from_display_module()

    def main(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
            self.player.update(events)
            self.screen.fill(TRANS)
            self.screen.blit(self.player.draw(), (0, 0))
            pygame.display.update()
            self.clock.tick(30)

    # Hacks to let me move the window
    @property
    def position(self):
        return self.window.position

    @position.setter
    def position(self, pos):
        if self.position == pos:
            return
        self.window.position = pos

    # Hacks to get the current screen position of the mouse
    @property
    def screenmouse(self):
        return win32api.GetCursorPos()


def main():
    Game().main()


if __name__ == "__main__":
    main()
