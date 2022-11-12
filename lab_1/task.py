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
        self.y = randint(100, 700)
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
        """Прорисовка шарика."""
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
            return 100/self.r
        return 0

class MegaBall(Ball):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)

        self.vx *= 2
        self.vy *= 2
        self.r = randint(50, 60)
        self.increase = 300

    def draw(self):
        """Прорисовка мегашарика"""
        circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )
        circle(
            self.screen,
            (255, 255, 255),
            (self.x, self.y),
            self.r,
            5
        )

    def click(self, event):
        """Проверка попадения клика на шарик"""
        if (self.x - event.pos[0])**2 + (self.y - event.pos[1])**2 <= self.r**2:
            print("You got it")
            self.vx *= 1.2
            self.vy *= 1.2
            self.r *= 0.9
            self.increase += 100
            return self.increase/self.r
        return 0
        
def draw_points(screen, points):
    """Прорисовка количества очков"""
    text = my_font.render(
        "Количество очков: " + str(round(points, 2)),
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
epic_ball = MegaBall(screen)    
    
while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print('Click!')
            for b in balls:
                points += b.click(event)
            points += epic_ball.click(event)
                    

    for b in balls:
        b.move()
        b.draw()
    draw_points(screen, points)
    epic_ball.draw()
    epic_ball.move()
    
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
