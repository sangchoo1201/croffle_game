import math
import random

from typing import cast

from script.scene import *
from script.text import TextRender
from script.flying import Flying

KEYMAP = {pygame.K_UP: -1, pygame.K_DOWN: 1}


class Title(Scene):
    def __init__(self, screen: pygame.Surface):
        from script.scene.bake import Bake
        from script.scene.eat import Eat
        from script.scene.result import Result

        super().__init__(screen)
        self.render = TextRender(screen, size=42, color=(24, 24, 30))

        self.options = ["크로플 굽기", "크로플 받아먹기", "리더보드 확인"]
        self.descriptions = [
            "정확한 시간동안 버튼을 눌러 크로플을 알맞게 굽는 게임입니다.",
            "네 방향에서 날아오는 크로플 중 안 익은 것은 막고 익은 것은 받는 게임입니다.",
            "각 게임 별 최고기록을 확인합니다."
        ]
        self.descriptions = [*map(lambda x: self.render.get_image(x, size=18), self.descriptions)]
        self.selection = 0
        self.callback = [Bake, Eat, Result]

        self.title = pygame.image.load("resource/image/title.png").convert_alpha()
        self.title = pygame.transform.scale(self.title, (800, 800))
        self.timer = 0
        self.flying_group = pygame.sprite.Group()
        self.begin = False
        self.screen_saver = False

    def get_event(self) -> Optional[callback]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_TAB:
                self.screen_saver = not self.screen_saver
            if event.key == pygame.K_ESCAPE:
                if self.begin:
                    self.begin = False
                    continue
                return End
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if not self.begin:
                    self.begin = True
                    continue
                return self.callback[self.selection]
            if event.key in KEYMAP and self.begin:
                self.selection += KEYMAP[event.key]
                self.selection %= 3

    def run(self) -> Optional[callback]:
        result = self.get_event()
        if result is not None:
            return result

        self.timer += 0.05

        if random.random() > 0.95:
            Flying(self.flying_group)

        self.flying_group.update()
        sprites = cast(list[Flying], self.flying_group.sprites())
        for sprite in sorted(sprites, key=lambda x: x.scale):
            self.screen.blit(sprite.image, sprite.rect)

        if self.screen_saver:
            return

        if self.begin:
            for i in range(3):
                color = (220, 220, 20) if i == self.selection else (24, 24, 30)
                self.render(self.options[i], (960, 700 + 120 * i), color=color)
                if i == self.selection:
                    self.render.blit(self.descriptions[i], (960, 740 + 120 * i))
        else:
            self.render("스페이스 바를 눌러 시작", (960, 800))

        title_image = pygame.transform.rotate(self.title, math.sin(self.timer) * 7)
        title_rect = title_image.get_rect(center=(960, 360))
        self.screen.blit(title_image, title_rect)
