import time

from script.scene import *
from script.text import TextRender
from script.data import get_data


class Result(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.eat_data = get_data("eat")

        self.surface = pygame.Surface((1920, 1080))
        self.surface.fill((247, 247, 255))
        self.render = TextRender(self.surface, 60, color=(24, 24, 30))
        self.fixed_render = TextRender(self.surface, 42, font="D2Coding.ttf", color=(24, 24, 30))
        self.render("크로플 굽기", (530, 180))
        self.render("크로플 받아먹기", (1390, 180))
        for i, data in enumerate(get_data("bake")):
            name, score = data
            self.fixed_render(name, (390, 300 + 70 * i))
            self.fixed_render(f"{score:05.2f}", (670, 300 + 70 * i))
        for i, data in enumerate(get_data("eat")):
            name, score = data
            self.fixed_render(name, (1250, 300 + 70 * i))
            self.fixed_render(f"{-score:02d}", (1530, 300 + 70 * i))

        self.start_time = time.perf_counter()

    def get_event(self) -> Optional[callback]:
        from script.scene.title import Title

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                return Title

    def run(self) -> Optional[callback]:
        from script.scene.title import Title

        result = self.get_event()
        if result is not None:
            return result

        if time.perf_counter() - self.start_time > 10:
            return Title

        self.screen.blit(self.surface, (0, 0))
