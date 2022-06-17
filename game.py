# imports
import pygame
import colorama
from colorama import Fore
import pyautogui
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
pygame.display.set_caption('Game')

# import images
EXIT_IMG = pygame.image.load('exit_btn.png')
BLANK_IMG = pygame.image.load('blank_inp.png')

# colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# fonts
pygame.font.init()
FONT1 = pygame.font.SysFont("GohuFont NF", 92)

#current player
CUR_USR = 0

# points
USR_ONE_PTS = 0
USR_TWO_PTS = 0

# press only occurs once
PRESS_1 = False

# NOTE: remove text and circle cords in final
TEXT_X = 400
TEXT_Y = 400

CIRC_X = 100
CIRC_Y = 100

# ! == SQL / START ============================================================================================================================================

# empty space between startups
print('\n')

# prove start screen happened
print('(' + Fore.GREEN + 'START'  + Fore.WHITE + ') Game.py Started')
    
# SQL variables
con = sqlite3.connect('game_data')
cur = con.cursor()

# print player usernames
def player_username0():
    SELECT_Q0 = """SELECT * FROM game_data;"""
    cur.execute(SELECT_Q0)
    RECORD0 = cur.fetchall()
    print('{' + Fore.MAGENTA + 'INFO' + Fore.WHITE + '}', RECORD0)

print('(' + Fore.GREEN + 'START'  + Fore.WHITE + ') Users: '), player_username0()

# ! == SPRITES ============================================================================================================================================

# create key input
def key_input():
        
    # make variables global
    global CIRC_X
    global CIRC_Y

    # make event possible
    KEYS = pygame.key.get_pressed()
    
    # if key pressed:
    # move right
    if KEYS[pygame.K_d]:

        # change circle location
        CIRC_X = CIRC_X + 5

        # print to show input pressed
        #print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '}', 'Circle moved right.')

    # move left
    if KEYS[pygame.K_a]:

        # change circle location
        CIRC_X = CIRC_X - 5

        # print to show input pressed
        #print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '}', 'Circle moved right.')

    # move down
    if KEYS[pygame.K_s]:

        # change circle location
        CIRC_Y = CIRC_Y + 5

        # print to show input pressed
        #print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '}', 'Circle moved down.')

    # move up
    if KEYS[pygame.K_w]:

        # change circle location
        CIRC_Y = CIRC_Y - 5

        # print to show input pressed
        #print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '}', 'Circle moved up.')

    # reset
    if KEYS[pygame.K_TAB]:
        
        # reset circle location
        CIRC_X = 100
        CIRC_Y = 100 

        # print to show input pressed
        #print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '}', 'Circle reset.')

def plus_num():
    
    # make user points global
    global USR_ONE_PTS

    # add one point
    USR_ONE_PTS = USR_ONE_PTS + 1

    # print points
    print('[' + Fore.LIGHTYELLOW_EX + 'POINTS'  + Fore.WHITE + '] User ONE has:', USR_ONE_PTS, 'POINTS')

# create button class
class Button_Mouse():

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

        # click reset
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # print on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        # reset action
        return action

# create button class
class Button_CIRCLE():

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
        
        # timer
        self.last_update = pygame.time.get_ticks()
        
        # interval
        self.interval = 300  # 3 second

    # create draw class
    def draw(self):

        # define action
        action = False

        # define keys
        KEYS = pygame.key.get_pressed()

        # find collide point
        if self.rect.collidepoint(CIRC_X, CIRC_Y):
            # print('HOVER')    
            
            global PRESS_1
            NOW = pygame.time.get_ticks()

            if KEYS[pygame.K_RETURN] and PRESS_1 == False:

                # set action and clicked to true
                    PRESS_1 = True
                    self.clicked = True
                    action = True
                    
                    print('(' + Fore.LIGHTGREEN_EX + 'WAIT' + Fore.WHITE + ')', self.interval, 'Secs')

                    print('[' + Fore.LIGHTBLUE_EX + 'NOW' + Fore.WHITE + ']', NOW, '{' + Fore.LIGHTBLACK_EX + 'LAST' + Fore.WHITE + '}', self.last_update, '(' + Fore.LIGHTRED_EX + 'INTERVAL' + Fore.WHITE + ')', self.interval)


                    if NOW - self.interval > self.last_update:
                        
                        self.last_update = NOW
        
                        PRESS_1 = False

                        self.clicked = False

                        print('(' + Fore.LIGHTGREEN_EX + 'WAIT' + Fore.WHITE + ') Passed' )

        # print on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        # reset action
        return action


TEXT1 = FONT1.render('TEST', True, BLACK, WHITE)

TEXT1RECT = TEXT1.get_rect()

TEXT1RECT.center = (TEXT_X // 2, TEXT_Y // 2)

EXIT_B = Button_Mouse(1000, 500, EXIT_IMG, 0.5)

TEST_B = Button_CIRCLE(1000, 250, BLANK_IMG, 0.5)

# ! == MAINLOOP ============================================================================================================================================

# make RUN always equal true
RUN = True
while RUN:

    # fill background white
    WIN.fill(WHITE)

    # display the text on screen
    WIN.blit(TEXT1, TEXT1RECT)

    # exit button draw
    if EXIT_B.draw():

        # exit
        RUN = False

        # drop and exit SQL table
        print('(' + Fore.YELLOW + 'EXIT' + Fore.WHITE + ') Exit Button Pressed')
        cur.execute("DROP TABLE IF EXISTS game_data")
        print('(' + Fore.YELLOW + 'EXIT' + Fore.WHITE + ') Table Dropped')
        con.close()  

    if TEST_B.draw():
        print('{' + Fore.MAGENTA + 'INPUT' + Fore.WHITE + '} TEST ACTIVE')
        plus_num()

    key_input()

    pygame.draw.circle(WIN, RED, (CIRC_X, CIRC_Y), 40)

# ! == EVENT HANDLER ============================================================================================================================================
    # NOTE: still no fucking clue what this does

    # event handler
    CLOCK.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            RUN = False
            if RUN == False: 
                con.close()   
                print('(' + Fore.YELLOW + 'EXIT' + Fore.WHITE + ') Game closed')          
                exit()         

    # actually update screen
    pygame.display.update()

# mainloop end
pygame.quit()