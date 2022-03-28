from random import randrange
import tkinter as tk
from tkinter import messagebox

import pygame as pg


class Cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dir_x=1, dir_y=0, color=(255, 0, 0)):
        self.pos = start
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.color = color

    def move(self, dir_x, dir_y):
        self.dir_x = dir_x
        self.dir_y = dir_y
        self.pos = (self.pos[0] + self.dir_x, self.pos[1] + self.dir_y)

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows
        i = self.pos[0]
        j = self.pos[1]

        pg.draw.rect(surface, self.color, (i * dis + 1, j * dis + 1, dis - 2, dis - 2))
        if eyes:
            centre = dis // 2
            radius = 3
            center_0f_circle_1 = (i * dis + centre - radius, j * dis + 8)
            center_0f_circle_2 = (i * dis + dis - radius * 2, j * dis + 8)
            pg.draw.circle(surface, (0, 0, 0), center_0f_circle_1, radius)
            pg.draw.circle(surface, (0, 0, 0), center_0f_circle_2, radius)


class Snake(object):
    body = []
    turns = {}

    def __init__(self, color, pos):
        self.color = color
        self.head = Cube(pos)
        self.body.append(self.head)
        self.dir_x = 0
        self.dir_y = 1

    def __len__(self):
        return len(self.body)

    def __getitem__(self, key):
        return self.body[key]

    def move(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

            keys = pg.key.get_pressed()

            for _ in keys:
                if keys[pg.K_LEFT]:
                    self.dir_x = -1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.K_RIGHT]:
                    self.dir_x = 1
                    self.dir_y = 0
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.K_UP]:
                    self.dir_x = 0
                    self.dir_y = -1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                elif keys[pg.K_DOWN]:
                    self.dir_x = 0
                    self.dir_y = 1
                    self.turns[self.head.pos[:]] = [self.dir_x, self.dir_y]

                else:
                    pass  # Do nothing

        for i, c in enumerate(self.body):
            p = c.pos[:]
            if p in self.turns:
                turn = self.turns[p]
                c.move(turn[0], turn[1])
                if i == len(self.body) - 1:
                    self.turns.pop(p)
            else:
                if c.dir_x == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dir_x == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dir_y == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dir_y == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dir_x, c.dir_y)

    def reset(self, pos):
        self.head = Cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dir_x = 0
        self.dir_y = 1

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dir_x, tail.dir_y

        if dx == 1 and dy == 0:
            self.body.append(Cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(Cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(Cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dir_x = dx
        self.body[-1].dir_y = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(surface, True)
            else:
                c.draw(surface)


def draw_grid(width, rows, surface):
    size_btn = width // rows

    x = 0
    y = 0
    for _ in range(rows):
        x += size_btn
        y += size_btn

        pg.draw.line(surface, (255, 255, 255), (x, 0), (x, width))
        pg.draw.line(surface, (255, 255, 255), (0, y), (width, y))


def redraw_window(surface):
    global rows, width, snake, snack
    surface.fill((0, 0, 0))
    snake.draw(surface)
    snack.draw(surface)
    draw_grid(width, rows, surface)
    pg.display.update()


def place_apple(rows, item):
    positions = item.body
    while True:
        x = randrange(rows)
        y = randrange(rows)
        if len(list(filter(lambda z: z.pos == (x, y), positions))) > 0:
            continue
        else:
            break
    return (x, y)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()


def main():
    global width, rows, snake, snack
    width = 500
    rows = 20
    win = pg.display.set_mode((width, width))
    snake = Snake((187, 22, 32), (10, 10))
    snack = Cube(place_apple(rows, snake), color=(0, 255, 61))
    RUNNING = True
    DELAY = 75
    clock = pg.time.Clock()

    while RUNNING:
        pg.time.delay(DELAY)
        clock.tick(10)
        snake.move()
        length = len(snake)
        DELAY -= 5 * (length // 2)
        if snake[0].pos == snack.pos:
            snake.add_cube()
            snack = Cube(place_apple(rows, snake), color=(0, 255, 61))

        for x in range(length):
            if snake[x].pos in list(map(lambda z: z.pos, snake[x + 1 :])):
                # print("[Score]", length)
                message_box("Game Over!", f"Your score: {length}")
                snake.reset((10, 10))
                break
        redraw_window(win)


if __name__ == "__main__":
    print("[Loading] Game starting...")
    # pg.time.delay(randrange(1000, 3000))
    main()
