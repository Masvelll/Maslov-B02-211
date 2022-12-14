import math
from random import choice, randint

import pygame


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.g = 1
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.x += self.vx
        self.y -= self.vy
        self.vy = self.vy - self.g
        if self.y >= 580 or self.y <= 0:
            self.vy = - self.vy
            self.live -= 10
        if self.x >= 800 or self.x <= 0:
            self.vx = - self.vx
            self.live -= 10
            

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        #print(self.x, obj.x, self.y, obj.y, self.r, obj.r)
        #print(((self.x - obj.x)**2 + (self.y - obj.y)**2)**(1/2), obj.r + self.r)
        if ((self.x - obj.x)**2 + (self.y - obj.y)**2)**(1/2) <= obj.r + self.r:
            #print("True")
            return True
        return False


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.pos1 = (0, 450)
        self.pos2 = (40, 450)
        self.length = 70
        

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[0]-20 != 0:
                self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):

        """Прорисовка пушки"""
        #print(self.pos1, self.pos2, (self.pos2[0] * self.f2_power/100, self.pos2[1] * self.f2_power/100))
        pygame.draw.line(self.screen, GREY, self.pos1, self.pos2, 7)

        """Прорисовка зарядки пушки"""
        pos_red1 = self.pos1[0] + self.length * math.cos(self.an) * self.f2_power / 100
        pos_red2 = self.pos1[1] + self.length * math.sin(self.an) * self.f2_power / 100
        pygame.draw.line(self.screen, self.color, self.pos1, (pos_red1, pos_red2), 7)

    def power_up(self):
        self.pos2 = (self.pos1[0] + self.length * math.cos(self.an), self.pos1[1] + self.length * math.sin(self.an))
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY
        


class Target:

    def __init__(self, screen, x=400, y=400):
        self.points = 0
        self.live = 1
        self.new_target()
        self.screen = screen
        self.color = RED
        self.x = x
        self.y = y
        self.r = 10

    def new_target(self):
        """ Инициализация новой цели. """
        x = self.x = randint(600, 780)
        y = self.y = randint(300, 550)
        r = self.r = randint(2, 50)
        color = self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points   

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target(screen)
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

    for b in balls:
        b.move()
        if b.hittest(target) and target.live:
            #print("worked")
            target.hit()
            target.new_target()
            balls.remove(b)
        if b.live <= 0:
            balls.remove(b)
    gun.power_up()

pygame.quit()
