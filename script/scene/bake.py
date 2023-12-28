import time

import pygame

from script.scene import *
from script.text import TextRender
from script.state import state


class Bake(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.render = TextRender(self.screen, 28, color=(24, 24, 30))
        self.timer = TextRender(self.screen, 48, font="D2Coding.ttf", color=(24, 24, 30))
        self.phase = 0

        self.closed = pygame.image.load("resource/image/closed.png").convert_alpha()
        self.opened = pygame.image.load("resource/image/opened.png").convert_alpha()

        self.dough = pygame.image.load("resource/image/dough.png").convert_alpha()
        self.dough = pygame.transform.scale(self.dough, (300, 225))
        self.croffle = pygame.image.load("resource/image/croffle.png").convert_alpha()
        self.croffle = pygame.transform.scale(self.croffle, (300, 225))
        self.dust = pygame.image.load("resource/image/dust.png").convert_alpha()
        self.dust = pygame.transform.scale(self.dust, (300, 225))

        self.result = pygame.Surface((0, 0))
        self.start_time = 0
        self.duration = 0

    def get_event(self) -> Optional[callback]:
        from script.scene.title import Title

        for event in pygame.event.get():
            from script.scene.name import Name

            if event.type == pygame.QUIT:
                return End
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE and self.phase == 1:
                self.phase = 2
                self.duration = time.perf_counter() - self.start_time
                if self.duration < 9.5:
                    self.result = self.dough
                elif self.duration <= 10.5:
                    self.result = self.croffle
                else:
                    self.result = self.dust
                continue
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return Title
            if event.key == pygame.K_SPACE:
                if self.phase == 0:
                    self.phase = 1
                    self.start_time = time.perf_counter()
                    continue
                if self.phase == 2:
                    state.score = abs(10 - self.duration)
                    state.game = "bake"
                    return Name

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result

        center = (960, 520)
        pos = (965, 690)

        if self.phase == 0:
            self.screen.blit(self.opened, self.opened.get_rect(center=center))
            self.screen.blit(self.dough, self.dough.get_rect(center=pos))
            self.render("10초간 스페이스 바를 누르고 10초가 지나면 스페이스 바를 떼세요!", (960, 970))
        if self.phase == 1:
            self.screen.blit(self.closed, self.closed.get_rect(center=center))
            t = time.perf_counter() - self.start_time
            alpha = 255 if t < 1.5 else max((2.5 - t) * 255, 0)
            self.timer(f"{t:05.2f}", (960, 950), alpha=alpha)
            alpha = 0 if t < 1.5 else min((t - 1.5) * 255, 255)
            self.timer("??.??", (960, 950), alpha=alpha)
        if self.phase == 2:
            self.screen.blit(self.opened, self.opened.get_rect(center=center))
            self.screen.blit(self.result, self.result.get_rect(center=pos))
            self.timer(f"{self.duration:05.2f}", (960, 950))
