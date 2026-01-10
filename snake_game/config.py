import pygame as pg

class Config:
    """Game configuration constants"""
    SCREEN_HEIGHT = 500
    SCREEN_WIDTH = 400
    CELL_SIZE = 10
    FPS = 15
    
    BACKGROUND = (255, 200, 175)
    BODY_INNER = (50, 175, 25)
    BODY_OUTER = (100, 100, 200)
    HEAD_COLOR = (0, 0, 0)
    FOOD_COLOR = (155, 45, 45)
    
    OPPOSITE = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
    DIRECTIONS = {
        pg.K_UP: "UP",
        pg.K_DOWN: "DOWN",
        pg.K_LEFT: "LEFT",
        pg.K_RIGHT: "RIGHT",
    }
    
    DELTA = {
        "UP": (0, -CELL_SIZE),
        "DOWN": (0, CELL_SIZE),
        "LEFT": (-CELL_SIZE, 0),
        "RIGHT": (CELL_SIZE, 0),
    }