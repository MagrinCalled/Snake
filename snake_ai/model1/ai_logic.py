import pygame as pg
from enum import Enum
import numpy as np
import random


class Direction(Enum):
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4

class SnakeAI:
    def __init__(self, w=400, h=400):
        self.w = w
        self.h = h
        self.screen = pg.display.set_mode((self.w, self.h))
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont(None, 30)
        self.reset()

    def reset(self):
 
        self.direction = random.choice(list(Direction))


        margin = 30
        grid_size = 10

        safe_x_min = margin
        safe_x_max = self.w - margin
        safe_y_min = margin
        safe_y_max = self.h - margin

        x = random.randrange(safe_x_min // grid_size, safe_x_max // grid_size) * grid_size
        y = random.randrange(safe_y_min // grid_size, safe_y_max // grid_size) * grid_size

        self.body = [[x, y]]
        self._place_food()
        self.score = 0
        self.num_frames = 0

    def _place_food(self):
        x = np.random.randint(0, (self.w // 10)) * 10
        y = np.random.randint(0, (self.h // 10)) * 10
        self.food = [x, y]
        if self.food in self.body:
            self._place_food()

    def _move(self, action):
        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = directions[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = directions[(idx + 1) % 4]
        else:
            new_dir = directions[(idx - 1) % 4]
        
        self.direction = new_dir

        x, y = self.body[0]

        if self.direction == Direction.RIGHT:
            x += 10
        elif self.direction == Direction.LEFT:
            x -= 10
        elif self.direction == Direction.DOWN:
            y += 10
        elif self.direction == Direction.UP:
            y -= 10
        
        self.body.insert(0, [x, y])
    
    def check_collision(self, point=None):
        if point is None:
            point = self.body[0]
        x, y = point
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return True
        if point in self.body[1:]:
            return True
        return False

    
    def _update_ui(self):

        self.screen.fill((255, 200, 175))
        vision = self.get_dirs(grid_size=10)
        self._draw_vision(vision)

        for i, block in enumerate(self.body):
            color = (75, 75, 0) if i == 0 else (0, 255, 0)
            pg.draw.rect(self.screen, color, pg.Rect(block[0], block[1], 10, 10))
        
        pg.draw.rect(self.screen, (255, 0, 0), pg.Rect(self.food[0], self.food[1], 10, 10))

        vision_surface = pg.Surface((10, 10), pg.SRCALPHA)
        vision_surface.fill((128, 128, 128, 100))

        head_x, head_y = self.body[0]

        txt = 'Score : ' + str(self.score)
        img = self.font.render(txt, True, (0, 75, 75))
        self.screen.blit(img, (0, 0))
        pg.display.update()

    def one_frame(self, action, SPEED):
        reward = 0
        self.num_frames += 1
        

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
        x, y = self.body[0]

        d_prev = self.d_food()

        directions = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = directions.index(self.direction)
        if np.array_equal(action, [1, 0, 0]):
            new_dir = directions[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = directions[(idx + 1) % 4]
        else:
            new_dir = directions[(idx - 1) % 4]
        self.direction = new_dir

        if self.direction == Direction.RIGHT:
            x += 10
        elif self.direction == Direction.LEFT:
            x -= 10
        elif self.direction == Direction.DOWN:
            y += 10
        elif self.direction == Direction.UP:
            y -= 10

        new_head = [x, y]

        if self.check_collision(new_head) or self.num_frames > 150 * len(self.body):
            reward = -15
            return reward, True, self.score

        self.body.insert(0, new_head)

        if self.body[0] == self.food:
            self.score += 1
            reward = 20
            self._place_food()
        else:
            self.body.pop()

        d_new = self.d_food()

        if d_new < d_prev:
            reward += 0.05
        else:
            reward -= 0.1

        self._update_ui()
        self.clock.tick()

        return reward, False, self.score
    
    def d_food(self):
        head_x, head_y = self.body[0]
        food_x, food_y = self.food
        return abs(head_x - food_x) // 10 + abs(head_y - food_y) // 10
    
    def get_dirs(self, grid_size=10): #creates an 11 by 11 square centered at snake's head
        head_x, head_y = self.body[0]
        cells = []

        half = grid_size // 2

        for i in range(-half, half + 1):        #forward
            for j in range(-half, half + 1):  #sideways

                if self.direction == Direction.UP:
                    dx, dy = j * 10, -i * 10
                elif self.direction == Direction.DOWN:
                    dx, dy = -j * 10, i * 10
                elif self.direction == Direction.LEFT:
                    dx, dy = -i * 10, -j * 10
                elif self.direction == Direction.RIGHT:
                    dx, dy = i * 10, j * 10

                cells.append((head_x + dx, head_y + dy))

        return cells
    def _draw_vision(self, cells):
        overlay = pg.Surface((10, 10), pg.SRCALPHA)
        overlay.fill((150, 150, 150, 80))  # translucent grey

        for x, y in cells:
            if 0 <= x < self.w and 0 <= y < self.h:
                self.screen.blit(overlay, (x, y))
