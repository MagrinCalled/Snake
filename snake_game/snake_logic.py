import pygame as pg

class Snake:
    """Snake game logic and rendering"""
    def __init__(self, config):
        self.config = config
        self.body = [[config.SCREEN_WIDTH // 2, config.SCREEN_HEIGHT // 2]]
        self.direction = "UP"
        self.grow = False
        self.is_alive = True

    def move(self):
        dx, dy = self.config.DELTA[self.direction]
        new_head = [
            (self.body[0][0] + dx) % self.config.SCREEN_WIDTH,
            (self.body[0][1] + dy) % self.config.SCREEN_HEIGHT
        ]

        if new_head in self.body:
            self.is_alive = False

        if self.is_alive:
            self.body.insert(0, new_head)

            if not self.grow:
                self.body.pop()
            else:
                self.grow = False

    def draw(self, screen):
        for i, part in enumerate(self.body):
            inner = self.config.HEAD_COLOR if i == 0 else self.config.BODY_INNER
            pg.draw.rect(screen, self.config.BODY_OUTER, (*part, self.config.CELL_SIZE, self.config.CELL_SIZE))
            pg.draw.rect(
                screen,
                inner,
                (part[0] + 1, part[1] + 1, self.config.CELL_SIZE - 2, self.config.CELL_SIZE - 2),
            )

    def change_direction(self, new_dir):
        if new_dir != self.config.OPPOSITE[self.direction]:
            self.direction = new_dir