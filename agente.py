# encoding: utf-8

# importar librerías externas
import torch
import random
import numpy as np
from collections import deque

# importar ei fichero ai_game.py que es el fichero que hemos creado
from ai_game import SnakeGameAI, Direction, Point
# importar el fichero model.py
from model import Linear_QNet, QTrainer
# importar el helper.py para plotear
from helper import plot

# Definición de variables de importancia
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Aleatoriedad
        self.gamma = 0.9 # Ratio de descuento
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)


    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.x < game.head.x,  # food left
            game.food.x > game.head.x,  # food right
            game.food.y < game.head.y,  # food up
            game.food.y > game.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        # Esto es lo mismo que lo anterior pero menos tricky.
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Movimientos aleatorios: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            # Move es un indice para modificar el movimiento entre 
            # [1,0,0], [0,1,0] y [0,0,1]
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            # Aquí el índice lo generamos vía torch.
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


def train():
    # Variables para el ploteo
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    # Generar objetos de las clases
    agent = Agent()
    game = SnakeGameAI()
    while True:
        # Capturamos estado anterior (old)
        state_old = agent.get_state(game)

        # Generamos movimiento
        final_move = agent.get_action(state_old)

        # Realizamos el movimiento y capturamos valores
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # Entrenamos short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Almacenamos vía remember.
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Entrenamos long memory, ploteamos resultados
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            # Actualización del record
            if score > record:
                record = score
                agent.model.save()

            print('Juego', agent.n_games, 'Puntuación', score, 'Mejor puntuación:', record)
            # Ploteos
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

# Para arrancar el script vía función train.
if __name__ == '__main__':
    train()