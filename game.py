# imports
import pygame
import sqlite3
import sys
import os

# ! == VARIABLES ============================================================================================================================================

# settings
FPS = 60
FPSCLOCK = pygame.time.Clock()
HEIGHT, WIDTH = 1200, 600
WIN = pygame.display.set_mode((HEIGHT, WIDTH), 0, 60)
CLOCK = pygame.time.Clock()

# import images
EXIT_IMG = pygame.image.load('exit_btn.png')

# colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
pygame.font.init()
FONT1 = pygame.font.SysFont("GohuFont NF", 92)

# ! == SQL / START ============================================================================================================================================

# empty space between startups
print('\n')

# prove start screen happened
print('(START) Game.py Started')
    
# SQL variables
con = sqlite3.connect('game_data')
cur = con.cursor()

# player usernames
def player_usernames():
    SELECT_Q = """SELECT * FROM game_data;"""
    cur.execute(SELECT_Q)
    RECORD = cur.fetchall()
    print(RECORD)

print('(START) Users: '), player_usernames()

# ! == SPRITES ============================================================================================================================================

# create button class
class Button():

    # create init variables
    def __init__(self, x, y, image, scale):

        # make width & height image size
        width = image.get_width()
        height = image.get_height()

        # add scaling
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()

        # set position
        self.rect.topleft = (x, y)

        # set clicked false
        self.clicked = False

    # create draw class
    def draw(self):

        # define action
        action = False

        # mouse pos
        pos = pygame.mouse.get_pos()
        # print(pos)

        # find collide point
        if self.rect.collidepoint(pos):
            # print('HOVER')
            
            # click check
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked  == False:
                
                # set action and clicked to true
                self.clicked = True
                action = True
            
        # reset clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # print on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        # reset action
        return action


EXIT_B = Button(1000, 500, EXIT_IMG, 0.5)

# ! == MAINLOOP ============================================================================================================================================

# make RUN always equal true
RUN = True
while RUN:

    # fill background white
    WIN.fill(WHITE)

    # exit button draw
    if EXIT_B.draw():

        # exit
        RUN = False

        # drop and exit SQL table
        print('(EXIT) Exit Button Pressed')
        cur.execute("DROP TABLE IF EXISTS game_data")
        print('(EXIT) Table Dropped')
        con.close()  

# ! == EVENT HANDLER ============================================================================================================================================

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