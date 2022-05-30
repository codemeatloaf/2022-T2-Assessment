# imports
import pygame
import sqlite3
import sys
import os

# SQL variables
con = sqlite3.connect('game_data.db')
cur = con.cursor()

# SQL table create
cur.execute("CREATE TABLE IF NOT EXISTS game_data (usr_id INT, usr_nm TEXT)")
print('Table Created')

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

# load button images
START_IMG = pygame.image.load('start_btn.png')
EXIT_IMG = pygame.image.load('exit_btn.png')
BLANK_IMG = pygame.image.load('blank_inp.png')

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

        # hover check
        if self.rect.collidepoint(pos):
            # print('HOVER')
            
            # click check
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked  == False:
                
                # set action and clicked to true
                self.clicked = True
                action = True
            
                # print('CLICK')
            
        # reset clicked
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # print on screen
        WIN.blit(self.image, (self.rect.x, self.rect.y))

        # reset action
        return action

# print to show log-screen started
def start():
    
    # prove start screen happened
    print('Logscreen Started')

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

        # mouse button events
        for event in event_list:

            # find mouse and if above text area become active
            if event.type == pygame.MOUSEBUTTONDOWN and not self.active:

                # if mouse is colliding
                self.active = self.rect.collidepoint(event.pos)

            # if active and key pressed make key event
            if event.type == pygame.KEYDOWN and self.active:

                # return key
                if event.key == pygame.K_RETURN:
                    
                    self.active = False
                    pass
                
                # individual keys
                if event.key == pygame.K_q:
                    self.text += 'q'
                
                if event.key == pygame.K_w:
                    self.text += 'w'

                if event.key == pygame.K_e:
                    self.text += 'e'

                if event.key == pygame.K_r:
                    self.text += 'r'

                if event.key == pygame.K_t:
                    self.text += 't'

                if event.key == pygame.K_y:
                    self.text += 'y'

                if event.key == pygame.K_u:
                    self.text += 'u'

                if event.key == pygame.K_i:
                    self.text += 'i'

                if event.key == pygame.K_o:
                    self.text += 'o'

                if event.key == pygame.K_p:
                    self.text += 'p'

                if event.key == pygame.K_a:
                    self.text += 'a'

                if event.key == pygame.K_s:
                    self.text += 's'

                if event.key == pygame.K_d:
                    self.text += 'd'

                if event.key == pygame.K_f:
                    self.text += 'f'

                if event.key == pygame.K_g:
                    self.text += 'g'

                if event.key == pygame.K_h:
                    self.text += 'h'

                if event.key == pygame.K_j:
                    self.text += 'j'

                if event.key == pygame.K_k:
                    self.text += 'k'

                if event.key == pygame.K_l:
                    self.text += 'l'

                if event.key == pygame.K_z:
                    self.text += 'z'

                if event.key == pygame.K_x:
                    self.text += 'x'

                if event.key == pygame.K_c:
                    self.text += 'c'

                if event.key == pygame.K_v:
                    self.text += 'v'

                if event.key == pygame.K_b:
                    self.text += 'b'

                if event.key == pygame.K_n:
                    self.text += 'n'

                if event.key == pygame.K_m:
                    self.text += 'm'

                # delete key
                if event.key == pygame.K_BACKSPACE:
                    
                    self.text = self.text[:-1]

                    # test to see if delete is working
                    print("Length of text is now", (len(self.text)))

                # render text
                self.render_text()

# define sprites on screen
# start & exit buttons
START_B1 = Button(150, 300, START_IMG, 0.8)
START_B2 = Button(150, 100, START_IMG, 0.8)
EXIT_B = Button(1000, 500, EXIT_IMG, 0.5)

# input 1
BLANK_B1 = InputBox(500, 100, BLANK_IMG, 1)
TEXT_B1 = TextInputBox1(510, 110, 80, FONT1)
GROUP = pygame.sprite.Group(TEXT_B1)

# keep mainloop running
RUN = True

# show screen started
start()

# mainloop
while RUN:

    # fill background white
    WIN.fill(WHITE)

    # start button 1 draw
    if START_B1.draw():
        # open game.py
        os.system('python3 game.py')
        RUN = False
        exit()

    # start button 2 draw
    if START_B2.draw():
        # open game.py
        os.system('python3 game.py')
        RUN = False
        exit()

    # exit draw
    if EXIT_B.draw():

        # exit
        RUN = False

        # drop and exit SQL table
        cur.execute("DROP TABLE game_data")
        print('Table Dropped')
        con.close()  

    # input 1 draw
    BLANK_B1.draw()
    GROUP.draw(WIN)

    # input 2 draw
    #BLANK_B2.draw()
    #GROUP2.draw(WIN)

    # event handler
    CLOCK.tick(60)
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            RUN = False
            if RUN == False: 
                cur.execute("DROP TABLE game_data")
                print('Table Dropped')
                con.close()             
                exit()              
    GROUP.update(event_list)

    # actually update screen
    pygame.display.update()

# mainloop end
pygame.quit()
