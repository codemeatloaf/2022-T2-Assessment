# imports
import pygame
import sys
import random
import sqlite3
from constants import *

# pygame display
pygame.display.set_caption('Guessing Game')

# variables
FPS = 60
FPSCLOCK = pygame.time.Clock()
WIN = pygame.display.set_mode((HEIGHT, WIDTH), 0, 60)
BOARD_L = 8
SIZE = 60



# mainloop
pygame.init()

def start():
    print('Main Game Started')

def main():

    start()

    RUN = True

    while RUN:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
            if RUN == False:
                pygame.quit()


WIN.fill(WHITE)

cnt = 0
for i in range(1, BOARD_L+1):
    for z in range(1, BOARD_L+1):
        
        # check if current loop value is even
        if cnt % 2 == 0:
            pygame.draw.rect(WIN, WHITE, [SIZE*z, SIZE*i, SIZE, SIZE])
        else:
            pygame.draw.rect(WIN, BLACK, [SIZE*z, SIZE*i, SIZE, SIZE])
        cnt += 1

    # since theres an even number of squares go back one value
    cnt -= 1

# add a border 
pygame.draw.rect(WIN, BLACK, [SIZE, SIZE, BOARD_L*SIZE, BOARD_L*SIZE], 1)


# mainloop end
pygame.display.update()
FPSCLOCK.tick(FPS)
main()
