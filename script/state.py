import pygame


class State:
    def __init__(self):
        self.fps = 60
        self.score = 0
        self.game = ""

    @property
    def width(self) -> int:
        return pygame.display.get_window_size()[0]

    @property
    def height(self) -> int:
        return pygame.display.get_window_size()[1]

    @property
    def unit(self) -> int:
        return min(self.width // self.column, self.height // self.row)

    @property
    def left(self) -> int:
        return self.width // 2 - self.unit * self.column // 2

    @property
    def top(self) -> int:
        return self.height // 2 - self.unit * self.row // 2

    @property
    def right(self) -> int:
        return self.width // 2 + self.unit * self.column // 2

    @property
    def bottom(self) -> int:
        return self.height // 2 + self.unit * self.row // 2


state = State()
