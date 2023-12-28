import pygame

from script.scene import Scene, End
from script.scene.title import Title
from script.state import state

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()

scene: Scene = Title(screen)

while True:
    screen.fill((247, 247, 255))

    result = scene.run()
    if result is not None:
        if result is End:
            pygame.quit()
            break
        scene = result(screen)
    else:
        pygame.display.update()

    clock.tick(state.fps)
