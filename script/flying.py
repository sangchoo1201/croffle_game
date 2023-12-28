import math
import random

import pygame


class Flying(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group):
        super().__init__(group)
        angle = math.radians(random.randrange(360))
        self.pos = pygame.math.Vector2(960, 540) + pygame.math.Vector2(math.cos(angle), math.sin(angle)) * 1200
        angle += math.radians(random.normalvariate(180, 20))
        self.speed = pygame.math.Vector2(math.cos(angle), math.sin(angle)) * (random.random() * 3 + 3)
        self.angle = 0
        self.rotate = random.normalvariate(0, 3.5)
        if random.random() > 0.97:
            self.speed *= 5
        if random.random() > 0.95:
            self.rotate *= 10
        self.scale = max(random.normalvariate(0.25, 0.05), 0.05)

        image = "croffle" if random.random() > 0.25 else "dough"
        self.original_image = pygame.image.load(f"resource/image/{image}.png").convert_alpha()
        self.original_image = pygame.transform.scale_by(self.original_image, self.scale)
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.timer = 1200

    def update(self):
        self.timer -= 1
        if self.timer == 0:
            self.kill()
            return
        self.pos += self.speed
        self.angle += self.rotate
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
