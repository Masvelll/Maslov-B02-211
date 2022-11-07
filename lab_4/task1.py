import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
screen.fill((100, 100, 100))

# Body
circle(screen, (240, 240, 0), (200, 175), 100)
circle(screen, (0, 0, 0), (200, 175), 100, 5)

# Left eye
circle(screen, (0, 0, 0), (150, 150), 20, 5)
circle(screen, (240, 0, 0), (150, 150), 18)
circle(screen, (0, 0, 0), (150, 150), 5) # <-- this

# Right eye
circle(screen, (0, 0, 0), (250, 150), 15, 5)
circle(screen, (240, 0, 0), (250, 150), 13)
circle(screen, (0, 0, 0), (250, 150), 5) # <-- and this have the same size
                                         # but in the picture it seems different :0

# mouth and brows
rect(screen, (0, 0, 0), (150, 210, 100, 10))
line(screen, (0, 0, 0), (110, 100), (180, 140), 10)
line(screen, (0, 0, 0), (290, 100), (220, 140), 10)


pygame.display.update()
clock = pygame.time.Clock()

finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()


