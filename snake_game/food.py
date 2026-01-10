import pygame as pg
import numpy as np

class Food:
    """Food that the snake eats"""
    def __init__(self, config, snake_body):
        self.config = config
        self.font = pg.font.SysFont('segoe ui emoji', config.CELL_SIZE)
        self.img = self.font.render('🍎', True, (255, 0, 0))
        self.respawn(snake_body)

    def respawn(self, snake_body):
        for _ in range(50):
            self.pos = [
                self.config.CELL_SIZE * np.random.randint(0, self.config.SCREEN_WIDTH // self.config.CELL_SIZE),
                self.config.CELL_SIZE * np.random.randint(0, self.config.SCREEN_HEIGHT // self.config.CELL_SIZE),
            ]
            if self.pos not in snake_body:
                break

    def draw(self, screen):
        screen.blit(self.img, self.pos)