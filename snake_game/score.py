import pygame as pg

class Score:
    """Score display and tracking"""
    def __init__(self):
        self.value = 0
        self.font = pg.font.SysFont(None, 30)

    def draw(self, screen):
        txt = 'Score : ' + str(self.value)
        img = self.font.render(txt, True, (0, 75, 75))
        screen.blit(img, (0, 0))