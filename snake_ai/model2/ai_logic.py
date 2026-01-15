import pygame as pg
from enum import Enum
import numpy as np
import random

class Direction(Enum):
    RIGHT = 1; DOWN = 2; LEFT = 3; UP = 4

class SnakeAI:
    def __init__(self, w=400, h=400):
        self.w, self.h = w, h
        self.screen = pg.display.set_mode((w, h))
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 30)
        self.grid = 10
        self.reset()

    def reset(self):
        self.direction = random.choice(list(Direction))
        margin = 30
        x = random.randrange(margin//self.grid, (self.w - margin)//self.grid) * self.grid
        y = random.randrange(margin//self.grid, (self.h - margin)//self.grid) * self.grid
        self.body, self.score, self.num_frames = [[x, y]], 0, 0
        self._place_food()

    def _place_food(self):
        self.food = [np.random.randint(0, self.w//self.grid)*self.grid,
                     np.random.randint(0, self.h//self.grid)*self.grid]
        if self.food in self.body: self._place_food()

    def _move(self, action):
        dirs = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = dirs.index(self.direction)

        self.direction = dirs[idx if np.array_equal(action,[1,0,0])
                              else (idx+1)%4 if np.array_equal(action,[0,1,0])
                              else (idx-1)%4]
        
        dx, dy = {Direction.RIGHT:(self.grid,0), Direction.LEFT:(-self.grid,0),
                  Direction.UP:(0,-self.grid), Direction.DOWN:(0,self.grid)}[self.direction]
        
        self.body.insert(0, [self.body[0][0]+dx, self.body[0][1]+dy])

    def check_collision(self, point=None):
        if point is None: point = self.body[0]

        x, y = point
        
        return x < 0 or x >= self.w or y < 0 or y >= self.h or point in self.body[1:]

    def one_frame(self, action, SPEED):
        self.num_frames += 1
        for e in pg.event.get():
            if e.type == pg.QUIT: pg.quit(); quit()
        self._move(action)
        head = self.body[0]
        if self.check_collision() or self.num_frames > 75 * len(self.body): return -15, True, self.score

        if head == self.food: self.score += 1; self._place_food(); reward=20
        
        else: self.body.pop(); reward=0
        
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward, False, self.score

    def _update_ui(self):
        self.screen.fill((255, 200, 175))

        for i, block in enumerate(self.body):
            color = (75, 75, 0) if i == 0 else (0, 255, 0)
            pg.draw.rect(self.screen, color, pg.Rect(block[0], block[1], self.grid, self.grid))

        pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(self.food[0], self.food[1], self.grid, self.grid))

        txt = 'Score : ' + str(self.score)
        img = self.font.render(txt, True, (0, 75, 75))
        self.screen.blit(img, (0, 0))

        pg.display.update()