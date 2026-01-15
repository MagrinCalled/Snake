import torch
import random
import numpy as np
from collections import deque
from ai_logic import SnakeAI, Direction
from rl_model import Linear_QNet, QTrainer
from helper import plot
import pygame as pg
import json
import os

STATS_FILE = './model/stats.json'
MAX_MEMORY = 100_000
MODEL_FILE = './model.pth'
BATCH_SIZE = 1000
LR = 0.001
SPEED = 500

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    else:
        return {"total_games": 0, "record": 0}

def save_stats(stats):
    os.makedirs(os.path.dirname(STATS_FILE), exist_ok=True)
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 512, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head_x, head_y = game.body[0]

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        danger_straight = (
            (dir_r and game.check_collision([head_x + 10, head_y])) or
            (dir_l and game.check_collision([head_x - 10, head_y])) or
            (dir_u and game.check_collision([head_x, head_y - 10])) or
            (dir_d and game.check_collision([head_x, head_y + 10]))
        )

        danger_right = (
            (dir_u and game.check_collision([head_x + 10, head_y])) or
            (dir_d and game.check_collision([head_x - 10, head_y])) or
            (dir_l and game.check_collision([head_x, head_y - 10])) or
            (dir_r and game.check_collision([head_x, head_y + 10]))
        )

        danger_left = (
            (dir_u and game.check_collision([head_x - 10, head_y])) or
            (dir_d and game.check_collision([head_x + 10, head_y])) or
            (dir_l and game.check_collision([head_x, head_y + 10])) or
            (dir_r and game.check_collision([head_x, head_y - 10]))
        )

        state = [danger_straight, danger_right, danger_left]

        state.extend([dir_l, dir_r, dir_u, dir_d])

        state.extend([game.food[0] < head_x, 
                      game.food[0] > head_x, 
                      game.food[1] < head_y, 
                      game.food[1] > head_y])

        return np.array(state, dtype=float)




    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state, total_games):
        final_move = [0, 0, 0]

        state0 = torch.tensor(state, dtype=torch.float)
        epsilon = 1 - (max(total_games, self.n_games) / 500)

        if epsilon > 0:
            if random.random() < epsilon:
                move = random.randint(0, 2)
            else:
                move = torch.argmax(self.model(state0)).item()
        else:
            move = torch.argmax(self.model(state0)).item()

        final_move[move] = 1
        return final_move, epsilon



def train():
    pg.init()
    plot_scores = []
    plot_mean_scores = []


    stats = load_stats()
    record = stats["record"]
    total_games = stats["total_games"]
    total_score = 0

    agent = Agent()
    agent.model.load(MODEL_FILE)
    game = SnakeAI()
    while True:

        state_old = agent.get_state(game)

        final_move, epsilon = agent.get_action(state=state_old, total_games=total_games)

        reward, done, score = game.one_frame(final_move, SPEED)
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:

            game.reset()
            agent.n_games += 1
            total_games += 1 
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
                print('Model Saved!')

            print('Score:', score, 'Record:', record,
                  'Total games:', total_games, *(["Epsilon: " + str(np.round(epsilon,2))] if epsilon > 0 else []))
            save_stats({"total_games": total_games, "record": record})

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()