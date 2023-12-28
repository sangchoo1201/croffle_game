import math
import random

import pygame

data = [
    ((220, 540), 0, (1, 0)),
    ((960, 1280), 90, (0, -1)),
    ((1700, 540), 180, (-1, 0)),
    ((960, -200), 270, (0, 1)),
]


class Bread(pygame.sprite.Sprite):
    def __init__(self, group: pygame.sprite.Group, speed: int):
        super().__init__(group)
        pos, angle, direction = random.choice(data)
        self.pos = pygame.math.Vector2(pos)
        self.speed = pygame.math.Vector2(direction) * speed

        self.cooked = random.random() > 0.4
        image = "croffle" if self.cooked else "dough"
        self.image = pygame.image.load(f"resource/image/{image}.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, angle, 0.2)
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image, threshold=127)

    def update(self):
        self.pos += self.speed
        self.rect = self.image.get_rect(center=self.pos)
