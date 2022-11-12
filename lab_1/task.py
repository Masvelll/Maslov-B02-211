import pygame
from pygame.draw import circle
from random import randint
pygame.init()

FPS = 30
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_name = pygame.font.match_font('droidsans')
my_font = pygame.font.Font(font_name, 30)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

class Ball():
    def __init__(self, screen: pygame.Surface):
        """Конструктор класса Ball."""

        self.screen = screen
        self.x = randint(100, 900)
        self.y = randint(100, 800)
        self.r = randint(10, 60)
        self.vx = randint(5, 10)
        self.vy = randint(5, 10)
        self.color = COLORS[randint(0, 5)]

    def move(self):
        """Перемещает мяч каждый тик."""

        self.x += self.vx
        self.y += self.vy

        if self.y + self.r >= HEIGHT or self.y - self.r <= 0:
            self.vy = -self.vy
        if self.x + self.r >= WIDTH or self.x - self.r <= 0:
            self.vx = -self.vx

    def draw(self):
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def click(self, event):
        """Проверка попадения клика на шарик."""
        if (self.x - event.pos[0])**2 + (self.y - event.pos[1])**2 <= self.r**2:
            print("You got it")
            return True

        
def draw_points(screen, points):
    """Прорисовка количества очков"""
    text = my_font.render(
        "Количество очков: " + str(points),
        True,
        (255, 255, 255)
    )
    screen.blit(text, (10, 10))


pygame.display.update()
clock = pygame.time.Clock()
finished = False
balls = []
points = 0

for i in range(5):
    b = Ball(screen)
    balls.append(b)
    
    
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            for b in balls:
                if b.click(event):
                    points += 1

    for b in balls:
        b.move()
        b.draw()
    draw_points(screen, points)
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
