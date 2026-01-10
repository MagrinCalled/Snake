import pygame as pg

class GameOver:
    """Game over screen and restart handling"""
    def __init__(self, config):
        self.config = config
        self.font_large = pg.font.SysFont(None, 75)
        self.font_small = pg.font.SysFont(None, 35)
        self.OVER = False

    def check_isover(self, snake):
        if not snake.is_alive:
            self.OVER = True

    def draw(self, score_value, screen, events):
        if self.OVER:
            game_over_txt = self.font_large.render('GAME OVER', True, (255, 0, 0))
            restart_txt = self.font_small.render('Press R to Restart', True, (0, 0, 0))
            score_txt = self.font_small.render(f'Score: {score_value}', True, (0, 0, 0))
            quit_txt = self.font_small.render('Press Q to Quit', True, (0, 0, 0))

            screen.blit(game_over_txt, (self.config.SCREEN_WIDTH // 2 - game_over_txt.get_width() // 2, self.config.SCREEN_HEIGHT // 3))
            screen.blit(score_txt, (self.config.SCREEN_WIDTH // 2 - score_txt.get_width() // 2, self.config.SCREEN_HEIGHT // 2 + 40))
            screen.blit(restart_txt, (self.config.SCREEN_WIDTH // 2 - restart_txt.get_width() // 2, self.config.SCREEN_HEIGHT // 2))
            screen.blit(quit_txt, (self.config.SCREEN_WIDTH // 2 - quit_txt.get_width() // 2, self.config.SCREEN_HEIGHT // 2 + 80))
        
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_r, pg.K_SPACE]:
                    return "RESTART"
                elif event.key in [pg.K_q, pg.K_ESCAPE]:
                    return "QUIT"
        return None