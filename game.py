# imports
import pygame
import sqlite3
import sys
import os

# variables
FPS = 60
FPSCLOCK = pygame.time.Clock()
HEIGHT, WIDTH = 1200, 600
WIN = pygame.display.set_mode((HEIGHT, WIDTH), 0, 60)
CLOCK = pygame.time.Clock()

# colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
pygame.font.init()
FONT1 = pygame.font.SysFont("GohuFont NF", 92)

# prove start screen happened
print('(START) Game.py Started')

    
# SQL variables
con = sqlite3.connect('game_data.db')
cur = con.cursor()

# show table at start
print('(START) Table on start:')
os.system('litecli -D game_data.db -e "select * from game_data"')

# keep mainloop running
RUN = True

# mainloop
while RUN:

    # fill background white
    WIN.fill(WHITE)

    pass

    # event handler
    CLOCK.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            RUN = False
            if RUN == False: 
                con.close()   
                print("(EXIT) Game closed")          
                exit()         

    # actually update screen
    pygame.display.update()

# mainloop end
pygame.quit()