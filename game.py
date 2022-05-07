from msilib.schema import Directory
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.Font('arial.ttf', 25)

# reset 

# reward

# play(action) - > dir

# game_iter

# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x, y') 

# rgb color
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)
RED = (200,0,0)

# Constants
BLOCKSIZE = 20
SPEED = 20


class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        #init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake.ai")
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head, Point(self.head.x-BLOCKSIZE,self.head.y),
                                Point(self.head.x-(BLOCKSIZE*2),self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
    
    def _place_food(self):
        x = random.randint(0, (self.w - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        y = random.randint(0, (self.h - BLOCKSIZE) // BLOCKSIZE) * BLOCKSIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. Collect User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT:
            #         self.direction = Direction.LEFT
            #     elif event.key == pygame.K_RIGHT:
            #         self.direction = Direction.RIGHT
            #     elif event.key == pygame.K_UP:
            #         self.direction = Direction.UP
            #     elif event.key == pygame.K_DOWN:
            #         self.direction = Direction.DOWN
                            
        # 2. move
        self._move(action) # Update the head
        self.snake.insert(0,self.head)

        # 3. Check if game is over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or jst move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        
        else:
            self.snake.pop()
        # 5.update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return gameover and score
        
        return reward, game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x, pt.y, BLOCKSIZE, BLOCKSIZE))
            pygame.draw.rect(self.display,BLUE1,pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x, self.food.y, BLOCKSIZE, BLOCKSIZE))

        text = font.render("Score : " + str(self.score), True, WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()
    
    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action,[1,0,0]):
            new_dir = clock_wise[idx]   # no change

        elif np.array_equal(action,[0,1,0]):
            nxt_idx = (idx + 1) % 4
            new_dir = clock_wise[nxt_idx]   # right turn r -> d -> l ->u

        else:
            nxt_idx = (idx - 1) % 4
            new_dir = clock_wise[nxt_idx]   #left turn r -> u -> l -> d
        
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCKSIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCKSIZE
        elif self.direction == Direction.UP:
            y -= BLOCKSIZE
        elif self.direction == Direction.DOWN:
            y += BLOCKSIZE
        
        self.head = Point(x,y)

    def is_collision(self, pt= None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - BLOCKSIZE or pt.x < 0 or pt.y > self.h - BLOCKSIZE or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True
        return False

# if __name__ == "__main__":
#     game = SnakeGameAI()

#     while True:
#         game_over, score = game.play_step()

#         if game_over == True:
#             break

#     print(f"Score: {score}")
#     pygame.quit()
