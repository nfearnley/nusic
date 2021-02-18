from pygame.sprite import Sprite

from functools import wraps


# Only run this method if one of the given attributes have changed
def uses(*attrs):
    oldvals = ()

    def wrapper(fn):
        @wraps(fn)
        def wrapped(self, *args, **kwargs):
            nonlocal oldvals
            newvals = tuple(getattr(self, name) for name in attrs)
            if oldvals != newvals:
                oldvals = newvals
                return fn(self, *args, **kwargs)
        return wrapped
    return wrapper


class Control(Sprite):
    def __init__(self, pos=(0, 0)):
        super().__init__()
        self.pos = pos

    def update(self, events):
        self.draw()

    @property
    def rect(self):
        return self.image.get_rect().move(*self.pos)
