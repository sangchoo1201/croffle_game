import random
import time
from typing import cast

import pygame.rect

from script.bread import Bread
from script.scene import *
from script.text import TextRender
from script.state import state

KEYMAP = {
    pygame.K_UP: pygame.rect.Rect(885, 435, 150, 10),
    pygame.K_DOWN: pygame.rect.Rect(885, 635, 150, 10),
    pygame.K_LEFT: pygame.rect.Rect(855, 465, 10, 150),
    pygame.K_RIGHT: pygame.rect.Rect(1055, 465, 10, 150),
}


class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = KEYMAP[pygame.K_UP]
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.mask = pygame.mask.from_surface(self.image, threshold=127)
        self.image.fill((24, 24, 30))

    def update(self, rect: pygame.rect.Rect):
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.mask = pygame.mask.from_surface(self.image, threshold=127)
        self.image.fill((24, 24, 30))


class Face(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.smile = pygame.image.load("resource/image/smile.png").convert_alpha()
        self.smile = pygame.transform.scale(self.smile, (150, 150))
        self.yum = pygame.image.load("resource/image/yum.png").convert_alpha()
        self.yum = pygame.transform.scale(self.yum, (150, 150))
        self.dead = pygame.image.load("resource/image/dead.png").convert_alpha()
        self.dead = pygame.transform.scale(self.dead, (150, 150))

        self.image = self.smile
        self.rect = self.image.get_rect(center=(960, 540))
        self.mask = pygame.mask.from_surface(self.image, threshold=127)

        self.timer = 0

    def eat(self):
        self.image = self.yum
        self.timer = 30

    def die(self):
        self.image = self.dead

    def update(self):
        if self.timer:
            self.timer -= 1
            if self.timer == 0:
                self.image = self.smile


class Eat(Scene):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.render = TextRender(self.screen, 28, color=(24, 24, 30))
        self.fixed_render = TextRender(self.screen, 60, font="D2Coding.ttf", color=(247, 247, 255))

        self.face = Face()
        self.bar = Bar()

        self.bread_group = pygame.sprite.Group()

        self.start_time = time.perf_counter()
        self.timer = 60
        self.speed = 5
        self.score = 0
        self.game_over = 0

    def get_event(self) -> Optional[callback]:
        from script.scene.title import Title

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return End
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return Title
            if event.key in KEYMAP and not self.game_over:
                self.bar.update(KEYMAP[event.key])

    def run(self) -> Optional[callback]:
        from script.scene.name import Name

        result = self.get_event()
        if result is not None:
            return result

        if self.timer == 0:
            self.timer = random.randint(40, 60)
            Bread(self.bread_group, self.speed)
            self.speed += 0.1
        else:
            self.timer -= 1

        if self.game_over:
            self.game_over -= 1
            if self.game_over == 0:
                state.score = -self.score
                state.game = "eat"
                return Name

            self.face.die()

            self.screen.blit(self.bar.image, self.bar.rect)
            self.screen.blit(self.face.image, self.face.rect)

            self.bread_group.draw(self.screen)

            pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 420, 1080))
            pygame.draw.rect(self.screen, (0, 0, 0), (1500, 0, 420, 1080))

            self.fixed_render(f"SCORE: {self.score:02d}", (50, 50), anchor="topleft")
            return

        self.bread_group.update()

        sprites = cast(list[Bread], self.bread_group)
        for bread in sprites:
            if pygame.sprite.collide_mask(self.bar, bread):
                if bread.cooked:
                    self.game_over = 120
                else:
                    self.score += 1
                    bread.kill()
            if pygame.sprite.collide_mask(self.face, bread):
                if bread.cooked:
                    self.score += 1
                    self.face.eat()
                    bread.kill()
                else:
                    self.game_over = 120

        self.face.update()

        self.screen.blit(self.bar.image, self.bar.rect)
        self.screen.blit(self.face.image, self.face.rect)

        t = time.perf_counter() - self.start_time
        if t < 5:
            self.render("안 익은 크로플만 막으세요!", (960, 700))

        self.bread_group.draw(self.screen)

        pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 420, 1080))
        pygame.draw.rect(self.screen, (0, 0, 0), (1500, 0, 420, 1080))

        self.fixed_render(f"SCORE: {self.score:02d}", (50, 50), anchor="topleft")
