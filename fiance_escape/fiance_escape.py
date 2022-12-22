import pygame
from webbrowser import open
from .maze import Maze
from .constants import *


class FianceEscape:
    def __init__(self, N=N):
        # Initializing game logic
        self.maze = Maze()

        pygame.init()  # initializing pygame

        # Screen is initialized with init_game method
        self.screen = None

        # Create a Font object
        self.font = pygame.font.SysFont('tlwgtypo', size=font_size, bold=True)

        # Init the mixer
        pygame.mixer.music.load('fiance_escape/media/jungle_groove.ogg')

        # Create an object to help update the grid
        self.clock = pygame.time.Clock()

        # Defining the Rects that will place the blocks on the screen
        self.rects = [pygame.Rect(grid_left + i * block_size, grid_top + j * block_size, block_size, block_size)
                      for j in range(n_elem)
                      for i in range(n_elem)]

        # Loading images used in the game
        self.bg = pygame.transform.scale(pygame.image.load('fiance_escape/media/bg.png'), size)

        sprite_sheet = pygame.image.load('fiance_escape/media/ground_tiles.png')

        self.path = pygame.transform.scale(sprite_sheet.subsurface((64, 0), (64, 64)), (block_size, block_size))
        self.wall = pygame.transform.scale(sprite_sheet.subsurface((128, 64), (64, 64)), (block_size, block_size))
        self.limit = pygame.transform.scale(sprite_sheet.subsurface((0, 64), (64, 64)), (block_size, block_size))

        self.button_play = pygame.transform.scale(pygame.image.load('fiance_escape/media/play.png'), button_size)
        self.button_play_rect = self.button_play.get_rect(midtop=(width / 2, self.rects[-1].bottom + spacing_buttons))

        self.button_info = pygame.transform.scale(pygame.image.load('fiance_escape/media/info.png'), button_size)
        self.button_info_rect = self.button_info.get_rect(bottomright=(width - grid_left,
                                                                       grid_top - 0.5 * spacing_buttons))

    def init_game(self):  # method that start the game
        # Creating a display Surface
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Fiance Escape")

        # Game background music
        pygame.mixer.music.play(-1)

        while True:
            self.main_screen()

    def main_screen(self):
        # Preparing the main screen
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.button_info, self.button_info_rect)
        self.display_grid()
        self.screen.blit(self.button_play, self.button_play_rect)

        pygame.display.flip()  # displaying the screen

        while True:
            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)  # leaving the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play_rect.collidepoint(event.pos):
                        return
                    if self.button_info_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

    def display_grid(self):
        # Clearing the area of the maze
        self.screen.blit(self.bg, self.rects[0].topleft, area=(self.rects[0].topleft, (maze_area, maze_area)))

        # Displaying fixed screen elements

        # Grid limits (superior and inferior)
        for i in range(n_elem):
            self.screen.blit(self.limit, self.rects[i])
            self.screen.blit(self.limit, self.rects[i + n_elem*(n_elem-1)])

        # Grid limits (side)
        for j in range(1, n_elem-2):
            self.screen.blit(self.limit, self.rects[j*n_elem])            
            self.screen.blit(self.limit, self.rects[j*n_elem + n_elem-1])

        self.screen.blit(self.limit, self.rects[n_elem*(n_elem-2)])            
        self.screen.blit(self.path, self.rects[n_elem*(n_elem-1) - 1])

        # Checking and displaying elements of the graph representing the maze
        # Horizontal paths
        for j in range(shape):
            for i in range(shape-1):
                i_pos, j_pos = self.grid_to_rect(i, j)

                self.screen.blit(self.path, self.rects[i_pos + j_pos*n_elem])

                if (self.maze[i + j*shape, i + j*shape + 1]):
                    self.screen.blit(self.path, self.rects[i_pos + j_pos*n_elem + 1])
                else:
                    self.screen.blit(self.wall, self.rects[i_pos + j_pos*n_elem + 1])
            
            self.screen.blit(self.path, self.rects[i_pos + 2 + j_pos*n_elem])

        # Vertical paths
        for j in range(shape-1):
            for i in range(shape-1):
                i_pos, j_pos = self.grid_to_rect(i, j)

                if (self.maze[i + j*shape, i + j*shape + shape]):
                    self.screen.blit(self.path, self.rects[i_pos + j_pos*n_elem + n_elem])
                else:
                    self.screen.blit(self.wall, self.rects[i_pos + j_pos*n_elem + n_elem])

                self.screen.blit(self.wall, self.rects[i_pos + 1 + j_pos*n_elem + n_elem])
            
            i_pos, j_pos = self.grid_to_rect(shape-1, j)

            if (self.maze[i + j*shape, i + j*shape + shape]):
                self.screen.blit(self.path, self.rects[i_pos + j_pos*n_elem + n_elem])
            else:
                self.screen.blit(self.wall, self.rects[i_pos + j_pos*n_elem + n_elem])

    @staticmethod
    # Transforms the identification in the graph to the grid of rects
    def grid_to_rect(i, j):
        return (1 + 2*i, 1 + 2*j)
