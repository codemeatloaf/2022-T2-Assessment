# imports
import pygame
import itertools

# colours
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# square generation
HEIGHT, WIDTH = 1200, 600
Rows, Cols = 8, 8
SQUARE_SIZE = Rows//Cols
BACKGROUND = pygame.Surface((WIDTH, HEIGHT))
COLOURS = itertools.cycle((WHITE, BLACK))
