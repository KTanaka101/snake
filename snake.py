__author__ = 'Tanaka'
import sys
import random
import pygame
from pygame.locals import *


SIZE = 20
WIDTH = 20
HEIGHT = 20


class Snake(object):

    def __init__(self, bait, length=None):
        if length is not None:
            self.length = length
            self.body = [SnakeParts() for _ in range(length)]
        else:
            self.length = 1
            self.body = [SnakeParts()]
        self. bait = bait

    def add_parts(self):
        self.body.append(SnakeParts(self.body[-1].x, self.body[-1].y))

    def up(self):
        next_y = self.body[0].y - 1
        if self.body[0].y == 0:
            return
        if self.is_my_body(self.body[0].x, next_y):
            return
        self._update()
        self.body[0].y = next_y
        self._judge()

    def right(self):
        next_x = self.body[0].x + 1
        if self.body[0].x == WIDTH-1:
            return
        if self.is_my_body(next_x, self.body[0].y):
            return
        self._update()
        self.body[0].x = next_x
        self._judge()

    def left(self):
        next_x = self.body[0].x - 1
        if self.body[0].x == 0:
            return
        if self.is_my_body(next_x, self.body[0].y):
            return
        self._update()
        self.body[0].x = next_x
        self._judge()

    def down(self):
        next_y = self.body[0].y + 1
        if self.body[0].y == HEIGHT-1:
            return
        if self.is_my_body(self.body[0].x, next_y):
            return
        self._update()
        self.body[0].y = next_y
        self._judge()

    def is_my_body(self, x, y):
        for parts in self.body:
            if parts.x == x and parts.y == y:
                return True

        return False

    def _judge(self):
        if self.body[0].x == self.bait.x and self.body[0].y == self.bait.y:
            self.add_parts()
            self.bait.update()

    def _update(self):
        for i in range(len(self.body)-1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

    def draw(self, screen):
        for parts in self.body:
            parts.draw(screen)


class SnakeParts(object):
    COLOR = (255, 0, 0)

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, Rect(self.x*SIZE, self.y*SIZE, SIZE, SIZE))


class GameField(object):
    BLACK = (0, 0, 0)
    GRAY = (230, 230, 230)

    def __init__(self, snake, bait, width=10, height=10):
        self.snake = snake
        self.bait = bait
        self.field = [[None for _ in range(width)] for _ in range(height)]

    def draw(self, screen):
        screen.fill(self.BLACK)
        for x in range(WIDTH):
            pygame.draw.line(screen, self.GRAY, (x*SIZE, 0), (x*SIZE, HEIGHT*SIZE))
        for y in range(HEIGHT):
            pygame.draw.line(screen, self.GRAY, (0, y*SIZE), (WIDTH*SIZE, y*SIZE))

        self.snake.draw(screen)
        self.bait.draw(screen)


class Bait(object):
    COLOR = (0, 255, 0)

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        self.x = random.randint(0, WIDTH-1)
        self.y = random.randint(0, HEIGHT-1)

    def draw(self, screen):
        pygame.draw.rect(screen, self.COLOR, Rect(self.x*SIZE, self.y*SIZE, SIZE, SIZE))


def run():
    rect = Rect(0, 0, 800, 600)
    pygame.init()
    sys.setrecursionlimit(10000)
    screen = pygame.display.set_mode(rect.size)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    bait = Bait()
    bait.update()
    snake = Snake(bait)
    game_field = GameField(snake, bait)

    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_w:
                    snake.up()
                elif event.key == K_d:
                    snake.right()
                elif event.key == K_a:
                    snake.left()
                elif event.key == K_s:
                    snake.down()

        game_field.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    sys.exit(run())