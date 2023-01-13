import pygame
from webbrowser import open
from .maze import Maze
from .fiancee import Fiancee
from .solvers import OnlineDFSAgent, LRTAStar
from .constants import *


class FianceEscape:
    def __init__(self, N=N):
        # Initializing game logic
        self.maze = Maze(N)
        self.fiancee = Fiancee((grid_left + block_side, grid_top + block_side))  # fiancee starting position is passed
        self.solver = None  # instantiated throughout the game

        pygame.init()  # initializing pygame

        # Screen is initialized with init_game method
        self.screen = None

        # Create a Font object
        self.font = pygame.font.SysFont('tlwgtypo', size=font_size, bold=True)

        # Init the mixer
        self.music_seeking = pygame.mixer.Sound('fiance_escape/media/jungle_groove.ogg')
        self.music_win = pygame.mixer.Sound('fiance_escape/media/win.ogg')

        self.channel_music = pygame.mixer.Channel(0)
        self.channel_effects = pygame.mixer.Channel(1)

        self.music_seeking.set_volume(0.5)

        # Object to save time to solve the maze
        self.clock = pygame.time.Clock()

        # Defining the Rects that will place the blocks on the screen
        self.rects = [pygame.Rect((grid_left + i*block_side, grid_top + j*block_side), block_size)
                      for j in range(n_elem)
                      for i in range(n_elem)]

        # Character movement logic
        self.rect_dest = {'u' : lambda place: self.rects[place - 2*n_elem].topleft,
                          'd' : lambda place: self.rects[place + 2*n_elem].topleft,
                          'r' : lambda place: self.rects[place+2].topleft,
                          'l' : lambda place: self.rects[place-2].topleft}

        self.movements = {'u' : lambda rect: (rect.left, rect.top-2),
                          'd' : lambda rect: (rect.left, rect.top+2),
                          'r' : lambda rect: (rect.left+2, rect.top),
                          'l' : lambda rect: (rect.left-2, rect.top)}

        # Loading images used in the game
        tiles = pygame.image.load('fiance_escape/media/ground_tiles.png')

        self.path = pygame.transform.scale(tiles.subsurface((64, 0), (64, 64)), block_size)
        self.wall = pygame.transform.scale(tiles.subsurface((128, 64), (64, 64)), block_size)
        self.limit = pygame.transform.scale(tiles.subsurface((0, 64), (64, 64)), block_size)
        self.unknown = pygame.transform.scale(tiles.subsurface((320, 0), (64, 64)), block_size)

        self.bg = self.load_bg('fiance_escape/media/bg.png')

        self.button_play = pygame.transform.scale(pygame.image.load('fiance_escape/media/play.png'), button_size)
        self.button_play_rect = self.button_play.get_rect(midtop=(width / 2, self.rects[-1].bottom + spacing_buttons))

        self.button_info = pygame.transform.scale(pygame.image.load('fiance_escape/media/info.png'), button_size)
        self.button_info_rect = self.button_info.get_rect(bottomright=(width - grid_left, grid_top - 0.5*spacing_buttons))

        self.button_return = pygame.transform.scale(pygame.image.load('fiance_escape/media/main.png'), button_size)
        self.button_return_rect = self.button_return.get_rect(bottomleft=(grid_left, grid_top - 0.5*spacing_buttons))

        self.button_update = pygame.transform.scale(pygame.image.load('fiance_escape/media/update.png'), button_size)
        self.button_update_rect = self.button_update.get_rect(bottomleft=(self.button_return_rect.right + 0.5*spacing_buttons,
                                                                          self.button_return_rect.bottom))

        self.button_solve = pygame.transform.scale(pygame.image.load('fiance_escape/media/solve.png'), button_size)
        self.button_solve.set_alpha(180)
        self.button_solve_rect = self.button_solve.get_rect(bottomleft=(self.button_update_rect.right + 0.5*spacing_buttons,
                                                                        self.button_update_rect.bottom))

        self.button_solve_2 = pygame.transform.scale(pygame.image.load('fiance_escape/media/solve.png'), button_size)
        self.button_solve_2_rect = self.button_solve_2.get_rect(bottomleft=(self.button_solve_rect.right + 0.5*spacing_buttons,
                                                                        self.button_return_rect.bottom))

        self.button_time = pygame.transform.scale(pygame.image.load('fiance_escape/media/time.png'), (2*button_side, button_side))
        self.button_time_rect = self.button_time.get_rect(midtop=(width / 2, self.rects[-1].bottom + spacing_buttons))

        self.button_win = pygame.transform.scale(pygame.image.load('fiance_escape/media/win.png'), (maze_area - 2*grid_left, maze_area // 5))
        self.button_win_rect = self.button_win.get_rect(topleft=(2*grid_left, grid_top + maze_area // 5 * 2))

    def init_game(self):  # method that start the game
        # Creating a display Surface
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Fiance Escape")

        while True:
            self.update()

            self.main_screen()
            self.play()

    def main_screen(self):
        # Preparing the main screen
        self.screen.blit(self.bg, (0, 0))

        self.screen.blit(self.button_info, self.button_info_rect)
        self.screen.blit(self.button_play, self.button_play_rect)

        pygame.display.flip()  # displaying the screen

        while True:
            # Getting input from user
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)  # leaving the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_play_rect.collidepoint(event.pos):
                        return
                    if self.button_info_rect.collidepoint(event.pos):
                        open('https://github.com/filipemedeiross/', new=2)

    def play(self):
        # Update the clock
        self.clock.tick()
        time = 0

        # Displaying fixed screen elements
        self.screen.blit(self.bg, (0, 0))  # overriding home screen buttons

        self.screen.blit(self.button_return, self.button_return_rect)
        self.screen.blit(self.button_update, self.button_update_rect)
        self.screen.blit(self.button_solve, self.button_solve_rect)
        self.screen.blit(self.button_solve_2, self.button_solve_2_rect)

        self.display_grid()
        self.screen.blit(self.fiancee.image, self.fiancee.rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.button_return_rect.collidepoint(event.pos):
                        return
                    if self.button_update_rect.collidepoint(event.pos):
                        self.update()  # update the game

                        self.clock.tick()
                        time = 0

                        self.display_grid()
                        self.screen.blit(self.fiancee.image, self.fiancee.rect)

                if not self.maze.won(self.fiancee.x, self.fiancee.y):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.button_solve_rect.collidepoint(event.pos):
                            self.solver = OnlineDFSAgent()
                        if self.button_solve_2_rect.collidepoint(event.pos):
                            self.solver = LRTAStar()

                    if self.solver:
                        while not self.maze.won(self.fiancee.x, self.fiancee.y):
                            place = self.grid_to_place(self.fiancee.x, self.fiancee.y)  # represents the place on the grid
                            action = self.solver.step_online(self.maze, self.fiancee.xy)

                            self.fiancee.move(action)
                            self.move_fiancee(action, place)
                    elif event.type == pygame.KEYDOWN:
                        pos = self.fiancee.x + self.fiancee.y*shape  # represents the vertex
                        place = self.grid_to_place(self.fiancee.x, self.fiancee.y)  # represents the place on the grid

                        action = None

                        if event.key == pygame.K_UP and self.maze[pos, pos-shape]:
                            action = 'u'
                        elif event.key == pygame.K_DOWN and self.maze[pos, pos+shape]:
                            action = 'd'
                        elif event.key == pygame.K_RIGHT and self.maze[pos, pos + 1]:
                            action = 'r'
                        elif event.key == pygame.K_LEFT and self.maze[pos, pos - 1]:
                            action = 'l'

                        if action:
                            self.fiancee.move(action)
                            self.move_fiancee(action, place)

                    if self.maze.won(self.fiancee.x, self.fiancee.y):
                        self.screen.blit(self.button_win, self.button_win_rect)

                        self.channel_music.stop()
                        self.channel_effects.play(self.music_win)
                    
            if not self.maze.won(self.fiancee.x, self.fiancee.y):
                # Game time
                time += self.clock.tick(10)
                self.display_time(time)

            pygame.display.flip()

    def load_bg(self, filename):
        background = pygame.transform.scale(pygame.image.load(filename), size)

        background.blit(pygame.transform.scale(self.path.copy(), maze_shape), self.rects[0].topleft)

        for rect in self.rects:
            background.blit(self.unknown, rect.topleft)

        return background

    def load_maze(self):
        # Maze background
        self.maze_surface = pygame.transform.scale(self.path.copy(), size)

        # Grid limits (superior and inferior)
        last_line = n_elem*(n_elem-1)
        for i in range(n_elem):
            self.maze_surface.blit(self.limit, self.rects[i])
            self.maze_surface.blit(self.limit, self.rects[i + last_line])

        # Grid limits (side)
        for j in range(1, n_elem-2):
            self.maze_surface.blit(self.limit, self.rects[j*n_elem])            
            self.maze_surface.blit(self.limit, self.rects[j*n_elem + n_elem - 1])

        self.maze_surface.blit(self.limit, self.rects[last_line - n_elem])            
        self.maze_surface.blit(self.path, self.rects[last_line - 1])

        # Checking and displaying elements of the graph representing the maze
        for j in range(shape):
            for i in range(shape):
                i_pos, j_pos = self.grid_to_rect(i, j)

                self.maze_surface.blit(self.path, self.rects[j_pos*n_elem + i_pos])

                if (i != shape-1):
                    if (self.maze[j*shape + i, j*shape + i + 1]):
                        self.maze_surface.blit(self.path, self.rects[j_pos*n_elem + i_pos + 1])
                    else:
                        self.maze_surface.blit(self.wall, self.rects[j_pos*n_elem + i_pos + 1])

                    if (j != shape-1):
                        self.maze_surface.blit(self.wall, self.rects[(j_pos+1)*n_elem + i_pos + 1])

                if (j != shape-1):
                    if (self.maze[j*shape + i, (j+1)*shape + i]):
                        self.maze_surface.blit(self.path, self.rects[(j_pos+1)*n_elem + i_pos])
                    else:
                        self.maze_surface.blit(self.wall, self.rects[(j_pos+1)*n_elem + i_pos])

    def display_grid(self):
        ref_pos = self.fiancee.rect.left - block_side, self.fiancee.rect.top - block_side

        # Hiding the area of the maze and showing known part
        self.screen.blit(self.bg, self.rects[0].topleft, (self.rects[0].topleft, maze_shape))
        self.screen.blit(self.maze_surface, ref_pos, (ref_pos, view_size))

    def move_fiancee(self, move, place):
        topleft = self.rect_dest[move](place)
        index = sprite_fiancee[move]
        
        i = index
        while self.fiancee.rect.topleft != topleft:
            self.fiancee.rect.topleft = self.movements[move](self.fiancee.rect)

            i += 1
            self.fiancee.update_image(i % 3 + index)

            self.display_grid()
            self.screen.blit(self.fiancee.image, self.fiancee.rect)

            pygame.display.flip()

    def display_time(self, time):
        time_text = self.font.render(f'{time // 1000 // 60}:{time // 1000 % 60}',
                                     True, COLOR_FONT)

        left = self.button_time_rect.centerx - time_text.get_width() / 2
        top = self.button_time_rect.centery - time_text.get_height() / 2

        self.screen.blit(self.button_time, self.button_time_rect)
        self.screen.blit(time_text, (left, top))

    def update(self):
        self.maze.update_maze()  # update the grid
        self.fiancee.reset()  # reset the fiance
        self.solver = None  # reset the solver
        self.load_maze()  # update the maze

        # Game background music
        if not self.channel_music.get_busy():
            self.channel_music.play(self.music_seeking, -1)
            
    @staticmethod
    def grid_to_rect(x, y):
        return (1 + 2*x, 1 + 2*y)  # transforms the (x, y) to the grid of rects

    def grid_to_place(self, x, y):
        x_pos, y_pos = self.grid_to_rect(x, y)

        return x_pos + y_pos*n_elem
