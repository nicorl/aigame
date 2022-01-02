# encoding: utf-8

# Librerías necesarias
import pygame
import random
from enum import Enum
from collections import namedtuple

# Arrancamos pygame
pygame.init()
fuente = pygame.font.Font('arial.ttf', 25)

# Definimos clases y variables que se utilizarán en el agente
class Direction(Enum):
    DERECHA = 1
    IZQUIERDA = 2
    ARRIBA = 3
    ABAJO = 4
    
Point = namedtuple('Point', 'x, y')

# Colores para la UI
BLANCO = (255, 255, 255)
ROJO = (200,0,0)
AZUL1 = (0, 0, 255)
AZUL2 = (0, 100, 255)
NEGRO = (0,0,0)

BLOCK_SIZE = 20
VELOCIDAD = 20

class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # Inicia pantalla
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
        # Inicia el estado del juego
        self.direction = Direction.DERECHA
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # 1. Captura input del usuario
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.IZQUIERDA
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.DERECHA
                elif event.key == pygame.K_UP:
                    self.direction = Direction.ARRIBA
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.ABAJO
        
        # 2. Mover la serpiente
        self._move(self.direction) # Actualiza la cabeza
        self.snake.insert(0, self.head)
        
        # 3. Comprueba si es game over ese movimiento
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. Genera nueva comida o mueve
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Actualiza UI y reloj
        self._update_ui()
        self.clock.tick(VELOCIDAD)

        # 6. Devuelve game_over y puntuación
        return game_over, self.score
    
    def _is_collision(self):
        # Golpe con los límites.
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # Golpe contra sí misma.
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(NEGRO)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, AZUL1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, AZUL2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, ROJO, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = fuente.render("Puntuacion: " + str(self.score), True, BLANCO)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.DERECHA:
            x += BLOCK_SIZE
        elif direction == Direction.IZQUIERDA:
            x -= BLOCK_SIZE
        elif direction == Direction.ABAJO:
            y += BLOCK_SIZE
        elif direction == Direction.ARRIBA:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Puntuación final', score)
        
        
    pygame.quit()