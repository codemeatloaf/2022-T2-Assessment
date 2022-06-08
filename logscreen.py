# imports
import pygame
import sqlite3
import sys
import os

# ! == Variables ============================================================================================================================================

# settings
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

# images
START_IMG = pygame.image.load('start_btn.png')
EXIT_IMG = pygame.image.load('exit_btn.png')
BLANK_IMG = pygame.image.load('blank_inp.png')

# text input
INPUT_TEXT1 = ""
INPUT_TRUE1 = False

INPUT_TEXT2 = ""
INPUT_TRUE2 = False

# prove start screen happened
print('(START) Logscreen.pys Started')

# ! == SQL / START ============================================================================================================================================

# SQL variables
con = sqlite3.connect('game_data')
cur = con.cursor()

# SQL table drop if already exists
cur.execute("DROP TABLE IF EXISTS game_data")
print('(START) Table Dropped')

# SQL table create if not exists
cur.execute("CREATE TABLE IF NOT EXISTS game_data (usr_id INT PRIMARY KEY, usr_nm TEXT)")
print('(START) Table Created')

# commit table
con.commit()
print('(START) Table Committed')

def player_usernames():
    SELECT_Q = """SELECT * FROM game_data;"""
    cur.execute(SELECT_Q)
    RECORD = cur.fetchall()
    print(RECORD)

# show table at start
print('(START) Table on start:'), player_usernames()

# ! == CLASSES ============================================================================================================================================

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

# text box outline
class InputBox():

    # create init variables
    def __init__(self, x, y, image, scale):
        width = 150
        height = 100
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    # draw input
    def draw(self):

        # print on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

# text box input 1
class TextInputBox1(pygame.sprite.Sprite):

    # create init variables
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None

        # mouse position
        self.pos = (x, y) 
        self.width = w

        # set font
        self.font = font

        # active is autofalse
        self.active = False

        # text is input
        self.text = ""

        # render the text
        self.render_text()

    # render text on screen
    def render_text(self):

        # define text surface
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)

        # make surface an image
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)

        # fill as backcolor
        if self.backcolor:
            self.image.fill(self.backcolor)

        # blit to surface
        self.image.blit(t_surf, (5, 5))

        # rectangle of text
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)

        # rectangle get pos
        self.rect = self.image.get_rect(topleft = self.pos)

    # update variables
    def update(self, event_list):

        # save information to database
        def save1():

            # set input text to global
            global INPUT_TEXT1
            global INPUT_TRUE1

            # check if save function started
            print("(SAVE) Save Function Started")

            # set input as username in database
            # execute command, where ? = self.text
            # VAR1 = Input
            VAR1 = INPUT_TEXT1
            INPUT_TRUE1 = True

            print('(SAVE) INPUT_TRUE1 = ', INPUT_TRUE1)

            cur.execute("INSERT OR REPLACE INTO game_data (usr_nm, usr_id) VALUES (?, 1)", (VAR1,))
            con.commit()

            # print to check if executed
            print('(SAVE) SQL Query executed')

            # print table update
            print('(SAVE) Table updated to:'), player_usernames()

        # mouse button events
        for event in event_list:

            # find mouse and if over text area become active
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                
                # if mouse is colliding
                self.active = self.rect.collidepoint(event.pos)

            # if active and key pressed make key event
            if event.type == pygame.KEYDOWN and self.active:

                # set INPUT_TEXT1 as global
                global INPUT_TEXT1
                global INPUT_TRUE1 
                    
                # return key
                if event.key == pygame.K_RETURN:

                    # start save function
                    if len(self.text) > 0:
                        save1()
                    else:
                        print('(SAVE) Not enough')

                    # exit input box
                    self.active = False

                # delete key
                if event.key == pygame.K_BACKSPACE:
                    
                    self.text = self.text[:-1]
                    INPUT_TEXT1 = INPUT_TEXT1[:-1]

                    # test to see if delete is working
                    print("(DELETE) Length of text is now", (len(self.text)))

                # input keys
                if event.key == pygame.K_q:

                    # add to self.text + input_text1
                    self.text += 'q'
                    INPUT_TEXT1 += 'q'
                        
                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Q) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Q) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Q) self.text is now:", self.text)
                        print("(OVERFILL Q) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_w:
                    self.text += 'w'
                    INPUT_TEXT1 += 'w'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL W) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL W) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL W) self.text is now:", self.text)
                        print("(OVERFILL W) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_e:
                    self.text += 'e'
                    INPUT_TEXT1 += 'e'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL E) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL E) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL E) self.text is now:", self.text)
                        print("(OVERFILL E) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_r:
                    self.text += 'r'
                    INPUT_TEXT1 += 'r'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL R) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL R) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL R) self.text is now:", self.text)
                        print("(OVERFILL R) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_t:
                    self.text += 't'
                    INPUT_TEXT1 += 't'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL T) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL T) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL T) self.text is now:", self.text)
                        print("(OVERFILL T) Input Text is now:", INPUT_TEXT1)
                        
                if event.key == pygame.K_y:
                    self.text += 'y'
                    INPUT_TEXT1 += 'y'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Y) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Y) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Y) self.text is now:", self.text)
                        print("(OVERFILL Y) Input Text is now:", INPUT_TEXT1) 

                if event.key == pygame.K_u:
                    self.text += 'u'
                    INPUT_TEXT1 += 'u'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL U) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL U) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL U) self.text is now:", self.text)
                        print("(OVERFILL U) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_i:
                    self.text += 'i'
                    INPUT_TEXT1 += 'i'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL I) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL I) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL I) self.text is now:", self.text)
                        print("(OVERFILL I) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_o:
                    self.text += 'o'
                    INPUT_TEXT1 += 'o'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL O) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL O) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL O) self.text is now:", self.text)
                        print("(OVERFILL O) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_p:
                    self.text += 'p'
                    INPUT_TEXT1 += 'p'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL P) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL P) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL P) self.text is now:", self.text)
                        print("(OVERFILL P) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_a:
                    self.text += 'a'
                    INPUT_TEXT1 += 'a'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL A) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL A) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL A) self.text is now:", self.text)
                        print("(OVERFILL A) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_s:
                    self.text += 's'
                    INPUT_TEXT1 += 's'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL S) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL S) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL S) self.text is now:", self.text)
                        print("(OVERFILL S) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_d:
                    self.text += 'd'
                    INPUT_TEXT1 += 'd'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL D) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL D) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL D) self.text is now:", self.text)
                        print("(OVERFILL D) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_f:
                    self.text += 'f'
                    INPUT_TEXT1 += 'f'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL F) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL F) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL F) self.text is now:", self.text)
                        print("(OVERFILL F) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_g:
                    self.text += 'g'
                    INPUT_TEXT1 += 'g'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL G) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL G) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL G) self.text is now:", self.text)
                        print("(OVERFILL G) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_h:
                    self.text += 'h'
                    INPUT_TEXT1 += 'h'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL H) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL H) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL H) self.text is now:", self.text)
                        print("(OVERFILL H) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_j:
                    self.text += 'j'
                    INPUT_TEXT1 += 'j'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL J) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL J) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL J) self.text is now:", self.text)
                        print("(OVERFILL J) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_k:
                    self.text += 'k'
                    INPUT_TEXT1 += 'k'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL K) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL K) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL K) self.text is now:", self.text)
                        print("(OVERFILL K) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_l:
                    self.text += 'l'
                    INPUT_TEXT1 += 'l'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL L) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL L) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL L) self.text is now:", self.text)
                        print("(OVERFILL L) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_z:
                    self.text += 'z'
                    INPUT_TEXT1 += 'z'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Z) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Z) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Z) self.text is now:", self.text)
                        print("(OVERFILL Z) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_x:
                    self.text += 'x'
                    INPUT_TEXT1 += 'x'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL X) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL X) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL X) self.text is now:", self.text)
                        print("(OVERFILL X) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_c:
                    self.text += 'c'
                    INPUT_TEXT1 += 'c'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL C) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL C) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL C) self.text is now:", self.text)
                        print("(OVERFILL C) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_v:
                    self.text += 'v'
                    INPUT_TEXT1 += 'v'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL V) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL V) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL V) self.text is now:", self.text)
                        print("(OVERFILL V) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_b:
                    self.text += 'b'
                    INPUT_TEXT1 += 'b'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL B) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL B) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL B) self.text is now:", self.text)
                        print("(OVERFILL B) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_n:
                    self.text += 'n'
                    INPUT_TEXT1 += 'n'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL N) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL N) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL N) self.text is now:", self.text)
                        print("(OVERFILL N) Input Text is now:", INPUT_TEXT1)

                if event.key == pygame.K_m:
                    self.text += 'm'
                    INPUT_TEXT1 += 'm'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL M) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT1 = INPUT_TEXT1[:-1]

                        # test to see if delete is working
                        print("(OVERFILL M) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL M) self.text is now:", self.text)
                        print("(OVERFILL M) Input Text is now:", INPUT_TEXT1)

                # render text
                self.render_text()

                #! END TEXTBOX ONE

# text box input 2
class TextInputBox2(pygame.sprite.Sprite):

    # create init variables
    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = (255, 255, 255)
        self.backcolor = None

        # mouse position
        self.pos = (x, y) 
        self.width = w

        # set font
        self.font = font

        # active is autofalse
        self.active = False

        # text is input
        self.text = ""

        # render the text
        self.render_text()

    # render text on screen
    def render_text(self):

        # define text surface
        t_surf = self.font.render(self.text, True, self.color, self.backcolor)

        # make surface an image
        self.image = pygame.Surface((max(self.width, t_surf.get_width()+10), t_surf.get_height()+10), pygame.SRCALPHA)

        # fill as backcolor
        if self.backcolor:
            self.image.fill(self.backcolor)

        # blit to surface
        self.image.blit(t_surf, (5, 5))

        # rectangle of text
        pygame.draw.rect(self.image, self.color, self.image.get_rect().inflate(-2, -2), 2)

        # rectangle get pos
        self.rect = self.image.get_rect(topleft = self.pos)

    # update variables
    def update(self, event_list):

        # save information to database
        def save2():

            # set input text to global
            global INPUT_TEXT2
            global INPUT_TRUE2

            # check if save function started
            print("(SAVE) Save Function Started")

            # set input as username in database
            # execute command, where ? = self.text
            # VAR2 = Input
            VAR2 = INPUT_TEXT2
            INPUT_TRUE2 = True

            print('(SAVE) INPUT_TRUE2 = ', INPUT_TRUE2)

            cur.execute("INSERT OR REPLACE INTO game_data (usr_nm, usr_id) VALUES (?, 2)", (VAR2,))
            con.commit()

            # print to check if executed
            print('(SAVE) SQL Query executed')

            # print table update
            print('(SAVE) Table updated to:'), player_usernames()

        # mouse button events
        for event in event_list:

            # find mouse and if over text area become active
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:
                
                # if mouse is colliding
                self.active = self.rect.collidepoint(event.pos)

            # if active and key pressed make key event
            if event.type == pygame.KEYDOWN and self.active:

                # set INPUT_TEXT2 as global
                global INPUT_TEXT2
                global INPUT_TRUE2 
                    
                # return key
                if event.key == pygame.K_RETURN:

                    # start save function
                    if len(self.text) > 0:
                        save2()
                    else:
                        print('(SAVE) Not enough')

                    # exit input box
                    self.active = False

                # delete key
                if event.key == pygame.K_BACKSPACE:
                    
                    self.text = self.text[:-1]
                    INPUT_TEXT2 = INPUT_TEXT2[:-1]

                    # test to see if delete is working
                    print("(DELETE) Length of text is now", (len(self.text)))

                # input keys
                if event.key == pygame.K_q:

                    # add to self.text + input_text2
                    self.text += 'q'
                    INPUT_TEXT2 += 'q'
                        
                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Q) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Q) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Q) self.text is now:", self.text)
                        print("(OVERFILL Q) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_w:
                    self.text += 'w'
                    INPUT_TEXT2 += 'w'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL W) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL W) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL W) self.text is now:", self.text)
                        print("(OVERFILL W) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_e:
                    self.text += 'e'
                    INPUT_TEXT2 += 'e'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL E) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL E) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL E) self.text is now:", self.text)
                        print("(OVERFILL E) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_r:
                    self.text += 'r'
                    INPUT_TEXT2 += 'r'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL R) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL R) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL R) self.text is now:", self.text)
                        print("(OVERFILL R) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_t:
                    self.text += 't'
                    INPUT_TEXT2 += 't'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL T) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL T) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL T) self.text is now:", self.text)
                        print("(OVERFILL T) Input Text is now:", INPUT_TEXT2)
                        
                if event.key == pygame.K_y:
                    self.text += 'y'
                    INPUT_TEXT2 += 'y'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Y) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Y) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Y) self.text is now:", self.text)
                        print("(OVERFILL Y) Input Text is now:", INPUT_TEXT2) 

                if event.key == pygame.K_u:
                    self.text += 'u'
                    INPUT_TEXT2 += 'u'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL U) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL U) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL U) self.text is now:", self.text)
                        print("(OVERFILL U) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_i:
                    self.text += 'i'
                    INPUT_TEXT2 += 'i'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL I) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL I) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL I) self.text is now:", self.text)
                        print("(OVERFILL I) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_o:
                    self.text += 'o'
                    INPUT_TEXT2 += 'o'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL O) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL O) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL O) self.text is now:", self.text)
                        print("(OVERFILL O) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_p:
                    self.text += 'p'
                    INPUT_TEXT2 += 'p'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL P) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL P) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL P) self.text is now:", self.text)
                        print("(OVERFILL P) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_a:
                    self.text += 'a'
                    INPUT_TEXT2 += 'a'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL A) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL A) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL A) self.text is now:", self.text)
                        print("(OVERFILL A) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_s:
                    self.text += 's'
                    INPUT_TEXT2 += 's'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL S) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL S) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL S) self.text is now:", self.text)
                        print("(OVERFILL S) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_d:
                    self.text += 'd'
                    INPUT_TEXT2 += 'd'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL D) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL D) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL D) self.text is now:", self.text)
                        print("(OVERFILL D) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_f:
                    self.text += 'f'
                    INPUT_TEXT2 += 'f'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL F) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL F) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL F) self.text is now:", self.text)
                        print("(OVERFILL F) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_g:
                    self.text += 'g'
                    INPUT_TEXT2 += 'g'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL G) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL G) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL G) self.text is now:", self.text)
                        print("(OVERFILL G) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_h:
                    self.text += 'h'
                    INPUT_TEXT2 += 'h'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL H) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL H) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL H) self.text is now:", self.text)
                        print("(OVERFILL H) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_j:
                    self.text += 'j'
                    INPUT_TEXT2 += 'j'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL J) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL J) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL J) self.text is now:", self.text)
                        print("(OVERFILL J) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_k:
                    self.text += 'k'
                    INPUT_TEXT2 += 'k'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL K) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL K) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL K) self.text is now:", self.text)
                        print("(OVERFILL K) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_l:
                    self.text += 'l'
                    INPUT_TEXT2 += 'l'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL L) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL L) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL L) self.text is now:", self.text)
                        print("(OVERFILL L) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_z:
                    self.text += 'z'
                    INPUT_TEXT2 += 'z'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL Z) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL Z) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL Z) self.text is now:", self.text)
                        print("(OVERFILL Z) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_x:
                    self.text += 'x'
                    INPUT_TEXT2 += 'x'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL X) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL X) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL X) self.text is now:", self.text)
                        print("(OVERFILL X) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_c:
                    self.text += 'c'
                    INPUT_TEXT2 += 'c'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL C) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL C) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL C) self.text is now:", self.text)
                        print("(OVERFILL C) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_v:
                    self.text += 'v'
                    INPUT_TEXT2 += 'v'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL V) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL V) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL V) self.text is now:", self.text)
                        print("(OVERFILL V) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_b:
                    self.text += 'b'
                    INPUT_TEXT2 += 'b'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL B) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL B) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL B) self.text is now:", self.text)
                        print("(OVERFILL B) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_n:
                    self.text += 'n'
                    INPUT_TEXT2 += 'n'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL N) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL N) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL N) self.text is now:", self.text)
                        print("(OVERFILL N) Input Text is now:", INPUT_TEXT2)

                if event.key == pygame.K_m:
                    self.text += 'm'
                    INPUT_TEXT2 += 'm'

                        # set length to  2
                    if len(self.text) > 3:
                
                        # print when length gets too much
                        print('(OVERFILL M) Length is:', len(self.text) + 1)

                        # remove single character
                        self.text = self.text[:-1]
                        INPUT_TEXT2 = INPUT_TEXT2[:-1]

                        # test to see if delete is working
                        print("(OVERFILL M) Length is now", (len(self.text)) + 1)
                        print("(OVERFILL M) self.text is now:", self.text)
                        print("(OVERFILL M) Input Text is now:", INPUT_TEXT2)

                # render text
                self.render_text()

                #! END TEXTBOX TWO

# ! == SPRITES ============================================================================================================================================

# define sprites on screen
# start & exit buttons
START_B1 = Button(150, 100, START_IMG, 0.8)
EXIT_B = Button(1000, 500, EXIT_IMG, 0.5)

# input 1
BLANK_B1 = InputBox(490, 90, BLANK_IMG, 1)
TEXT_B1 = TextInputBox1(500, 100, 80, FONT1)
GROUP1 = pygame.sprite.Group(TEXT_B1)

# input 2
BLANK_B2 = InputBox(490, 290, BLANK_IMG, 1)
TEXT_B2 = TextInputBox2(500, 300, 80, FONT1)
GROUP2 = pygame.sprite.Group(TEXT_B2)

# ! == MAINLOOP ============================================================================================================================================

# make RUN always equal true
RUN = True
while RUN:

    # fill background white
    WIN.fill(WHITE)

    # start button draw
    if START_B1.draw():
        
        if INPUT_TRUE1 == True:
            print('(START) Input1 passed')

            if INPUT_TRUE2 == True:
                print('(START) Input2 passed')

                # open game.py
                print('(START) Button 1 Pressed')
                os.system('python3 game.py')
                RUN = False
                exit()

            else:
                print('[ERROR] Input2 False')

        else:
            print('[ERROR] Input1 False')

    # exit button draw
    if EXIT_B.draw():

        # exit
        RUN = False

        # drop and exit SQL table
        print('(EXIT) Exit Button Pressed')
        cur.execute("DROP TABLE IF EXISTS game_data")
        print('(EXIT) Table Dropped')
        con.close()  

    # input 1 draw
    BLANK_B1.draw()
    GROUP1.draw(WIN)

    # input 2 draw
    BLANK_B2.draw()
    GROUP2.draw(WIN)

# ! == EVENT HANDLER ============================================================================================================================================

    # event handler
    CLOCK.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            RUN = False
            if RUN == False: 
                con.close()   
                print("(EXIT) Login closed")          
                exit()         

    GROUP1.update(event_list)
    GROUP2.update(event_list)

    # actually update screen
    pygame.display.update()

# mainloop end
pygame.quit()