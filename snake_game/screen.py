import pygame as pg

class Screen:
    """Game screen management"""
    def __init__(self, config):
        self.config = config
        self.WIDTH = (config.SCREEN_WIDTH // config.CELL_SIZE) * config.CELL_SIZE
        self.HEIGHT = (config.SCREEN_HEIGHT // config.CELL_SIZE) * config.CELL_SIZE
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))

    def draw_background(self):
        self.screen.fill(self.config.BACKGROUND)