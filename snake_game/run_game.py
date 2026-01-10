import pygame as pg
from .config import Config
from .snake_logic import Snake
from .food import Food
from .score import Score
from .screen import Screen
from .gameover import GameOver

class SnakeGame:
    """Main game controller"""
    def __init__(self, fps=15):
        self.config = Config()
        self.config.FPS = fps
        self.screen = Screen(self.config)
        self.clock = pg.time.Clock()
        self.reset_game()
        self.run()

    def reset_game(self):
        self.snake = Snake(self.config)
        self.food = Food(self.config, self.snake.body)
        self.score = Score()
        self.can_change = True
        self.game_over = GameOver(self.config)

    def run(self):
        """Main game loop"""
        running = True
        while running:
            self.screen.draw_background()
            events = pg.event.get()
            
            for event in events:
                if event.type == pg.QUIT:
                    running = False
                    pg.quit()
                    exit()
                
                if event.type == pg.KEYDOWN and self.can_change and not self.game_over.OVER:
                    new_dir = self.config.DIRECTIONS.get(event.key)
                    if new_dir:
                        self.snake.change_direction(new_dir)
                        self.can_change = False
            
            if not self.game_over.OVER:
                self.snake.move()
                self.game_over.check_isover(self.snake)
                
                if self.snake.body[0] == self.food.pos:
                    self.snake.grow = True
                    self.score.value += 1
                    self.food.respawn(self.snake.body)
                
                self.food.draw(self.screen.screen)
                self.snake.draw(self.screen.screen)
                self.score.draw(self.screen.screen)
                self.can_change = True
            else:
                self.food.draw(self.screen.screen)
                self.snake.draw(self.screen.screen)
                self.score.draw(self.screen.screen)
                action = self.game_over.draw(self.score.value, self.screen.screen, events)
                if action == "RESTART":
                    self.reset_game()
                elif action == "QUIT":
                    running = False
                    pg.quit()
                    exit()
            
            pg.display.update()
            self.clock.tick(self.config.FPS)